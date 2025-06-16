#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/6/16 9:59
# @Author  : caijian
# @File    : batch_msg.py
# @Software: PyCharm
import os
import time
import json
import requests
import pandas as pd
import re
# --- 配置 ---
API_URL = "http://127.0.0.1:8000/v1/chat/completions"
headers = {"Content-Type": "application/json"}
INPUT_CSV = "Random_Unique_PointName_Images.csv"
OUTPUT_CSV = "inference_results.csv"
MODEL = "gpt-4"
MAX_TOKENS = 500
SLEEP_INTERVAL = 0.5   # 两次请求之间暂停秒数，防止速率过快被限流

# 读取待推理的 CSV
df = pd.read_csv(INPUT_CSV, encoding="utf-8")
if "url" not in df.columns:
    raise ValueError(f"输入 CSV {INPUT_CSV} 中找不到 'url' 列")

results = []

with open("point_mapping.json", 'r', encoding='utf-8') as f:
    mapping = json.load(f)

mapping_str = json.dumps(mapping, ensure_ascii=False, indent=2)

# 定义 CSV 文件的列名
output_columns = [
    "url",
    "task_type_name",
    "point_type_name",
    "point_name",
    "pred_task_type",
    "pred_point_type",
    "pred_point_name" # 这里修正了原始代码中的重复 point_name 列
]

# 在循环开始前，如果输出文件不存在，则写入头部
# 如果文件已存在，则直接追加，不写入头部
OUTPUT_CSV = "inference_results.csv" 
if not os.path.exists(OUTPUT_CSV):
    pd.DataFrame(columns=output_columns).to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"创建新的输出文件: {OUTPUT_CSV}")
else:
    print(f"输出文件 {OUTPUT_CSV} 已存在，将追加数据。")


for idx, row in df.iterrows():
    image_url = row["url"]
    task_type_name=row['task_type_name']
    point_type_name =row['point_type_name']
    point_name =row['point_name']
    if (idx+1)%10==0:
        print(f"[{idx+1}/{len(df)}] 处理图片: {image_url}",flush=True)
    # 构造请求体
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": [
                    {"type": "text",     "text": f"""你是汽车图像分类专家。
下面给出了所有合法的二级点位类型(point_type_name) (辅助图,整体外观,其他细节)及其对应的三级点位名称(point_name)列表：
{mapping_str}
请你按照严格的三步推理流程，结合给定的图片，生成符合逻辑的推理过程：
1. 第一步：确认这是一张“外观”图片，并简要说明依据。
2. 第二步：从上述 point_type_name 列表中，选择最符合的那一项，并说明理由。
3. 第三步：在选中的 point_type_name 对应的点位名称列表里，选择最符合的 point_name，并说明理由。

在推理过程中，请确保你的解释和理由能够合理支持给定的答案。

最后，请仅输出一个有效 JSON：
{{"task_type": "外观", "point_type": "…", "point_name": "…"}}
请开始你的推理过程："""},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ],
        "max_tokens": MAX_TOKENS
    }

    # 4. 发送请求
    response = requests.post( "http://127.0.0.1:8000/v1/chat/completions", headers=headers, json=payload)
     # 5. 处理响应
    if response.status_code == 200:
        data = response.json()
        text = data["choices"][0]["message"]["content"]
        match = re.search(r'\{[^}]*\}', text)
        current_result = {
            "url": image_url,
            "task_type_name": task_type_name,
            "point_type_name": point_type_name,
            "point_name": point_name,
            "pred_task_type": "", # 默认值
            "pred_point_type": "", # 默认值
            "pred_point_name": "" # 默认值
        }
        if match:
            json_string = match.group(0)
            if (idx+1)%10==0:
                print("result:",json_string,flush=True)
            try:
                parsed = json.loads(json_string)
                current_result["pred_task_type"] = parsed.get("task_type", "")
                current_result["pred_point_type"] = parsed.get("point_type", "")
                current_result["pred_point_name"] = parsed.get("point_name", "")
            except json.JSONDecodeError:
                print(f"警告：无法解析 JSON 字符串: {json_string} for URL: {image_url}")
           
        else:
            print(f"请求失败，状态码：{response.status_code}",)
            print(response.text)
        pd.DataFrame([current_result], columns=output_columns).to_csv(
            OUTPUT_CSV, mode='a', header=False, index=False, encoding="utf-8-sig"
        )
        time.sleep(0.1)

print(f"\n全部完成，结果已保存到 {OUTPUT_CSV}")
