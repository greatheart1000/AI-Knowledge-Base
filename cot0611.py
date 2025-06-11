#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/6/11 15:58
# @Author  : caijian
# @File    : cot_0611.py
# @Software: PyCharm
# 将之前推理错的进行纠正，得到推理过程，然后与之前的推理进行结合 
import os
import json
import time
import pandas as pd
from openai import OpenAI
from tqdm import tqdm
import time
# 1. 初始化 Ark 客户端
client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key="4185fc5d-ec50-4667-bd93-d42e801fe3de",
)
with open("point_mapping.json", 'r', encoding='utf-8') as f:
    mapping = json.load(f)

mapping_str = json.dumps(mapping, ensure_ascii=False, indent=2)



df=pd.read_csv(r'C:\Users\great\Downloads\第四轮测试集图片识别结果.csv',encoding='gbk')
print(df.columns)
# 筛选出不匹配的行
mismatched_df = df.query('正确答案 != 预测答案')
# 遍历筛选出的每一行
print("使用 iterrows() 遍历不匹配的行：")

def make_user_message(image_url: str) -> list:
    return [
        {
            "type": "image_url",
            "image_url": {"url": image_url}
        },
        {
            "type": "text",
            "text": "请按照上面的指引，一步步推理并给出最终 JSON。"
        }
    ]
out_file = "reason_cot.jsonl"
fw = open(out_file, "w", encoding="utf-8")

for index, row in mismatched_df.iterrows():
    image_url = row['url']
    # prediction= row=['prediction']
    print(f"行索引: {index}")
    # print(f"正确答案: {row['正确答案']}, 预测答案: {row['预测答案']}")
    alist = row['正确答案'].split("-")
    if not row['预测答案'] or type(row['预测答案'])!=str:
        pass
    else:
        alist_ = row['预测答案'].split("-")
    correct_point_type =alist[1]
    correct_point_name =alist[-1]
    predicted_point_type = alist_[1]
    predicted_point_name = alist_[-1]
    # 你可以访问该行的其他列，例如：
    # print(f"其他列: {row['其他列名']}")
    SYSTEM_PROMPT = f"""
    你是汽车“外观”图像分类专家。
    下面给出了所有合法的二级点位类型point_type_name(辅助图,整体外观,其他细节)及其对应的三级点位名称(point_name)列表：
    {mapping_str}
    你的任务是分析给定图片的“正确答案”和“模型预测答案”，按照严格的纠错推理流程，生成符合逻辑的纠错过程。
    ---
    **纠错推理流程（Chain of Thought）**：
    1.  * 对比“正确答案”和“模型预测答案”中的 `point_type`。
        * 如果两者不一致，详细解释模型为什么预测错误，并从上述 `point_type_name` 列表中选择最符合正确答案的那一项，说明理由。
        * 如果两者一致，则略过此步，进入下一步。
    2.  **步骤二：根据给定的“正确答案”和“模型预测答案”中的 `point_name`，详细解释模型为什么预测错误，并解释为什么正确答案是合理的。
        * **特殊强调：方位判断**：如果 `point_name` 包含“前”、“后”、“左”、“右”、“侧”等方位词，请在推理中明确说明你是如何从图片中判断出具体方位的（例如，根据车辆整体朝向、车身参照物如方向盘/车门/引擎盖等）。
        * **特殊强调：关键特征识别**：如果 `point_name` 涉及具体设备（如“摄像头”、“雷达”、“传感器”）或特定数值（如“轮胎尺寸”），请在推理中描述你是如何在图片中识别这些关键特征的（例如，摄像头通常是小孔状，轮胎尺寸会有特定的数字和字母组合）。
        * 如果两者一致，则略过此步，进入下一步。
    在推理过程中，请确保你的解释和理由能够合理支持给定的正确答案。
    ---
    【输入图片URL】：{image_url}
    【正确答案】：
    {{"task_type": "外观", "point_type": "{correct_point_type}", "point_name": {correct_point_name}
    【模型预测答案】：
    {{"task_type": "外观", "point_type": "{predicted_point_type}", "point_name":{predicted_point_name}
    请开始你的纠错推理过程：
    最后，请仅输出一个有效 JSON：
    {{"task_type": "外观", "point_type": "{correct_point_type}", "point_name": "{correct_point_name}"，"reason":"待填"}}
    """
    try:
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        },
                    },
                    {"type": "text", "text": SYSTEM_PROMPT},
                ],
            }
        ]
        resp = client.chat.completions.create(
            model="doubao-1.5-vision-pro-250328",
            messages=messages,
            temperature=0.0,
            max_tokens=512,
        )
        cot = resp.choices[0].message.content.strip()
        # print(cot)
        record = {
                    "image_url": image_url ,
                    "task_type": "外观",
                     "point_type": correct_point_type,
                    "point_name": correct_point_name,
                      "model_cot": cot
                    }
        fw.write(json.dumps(record, ensure_ascii=False) + "\n")
        if (index+1)%100==0:
            print(cot)
            print("已进行了：",index+1)
        time.sleep(0.001)
    except Exception as e:
        print(e)
        time.sleep(0.005)

#读取生成的jsonl 然后与之前的进行组合成强化学习的数据集 
num =0
with open('reason_cot.jsonl' , 'r',encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        image_url = data['image_url']
        task_type='外观'
        point_type =data['point_type']
        point_name =data['point_name']
        model_cot= data['model_cot']
        # 正则表达式模式
        cleaned_model_cot = model_cot.replace('\n', '').replace('\r', '')
        cleaned_model_cot = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', cleaned_model_cot)  # 移除ASCII控制字符和扩展ASCII控制字符
        parsed_cot = json.loads(cleaned_model_cot)
        print(parsed_cot['reason'])
