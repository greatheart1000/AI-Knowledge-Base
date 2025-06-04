#######这个文件就是生产COT数据集的代码

import os
import json
import time
import pandas as pd
from openai import OpenAI
from tqdm import tqdm
import re
import logging

# 1. 配置日志
logging.basicConfig(
    level=logging.INFO,  # 你可以改成 DEBUG
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("output.log", encoding='utf-8'),
        logging.StreamHandler()  # 同时输出到控制台
    ]
)

# 1. 初始化 Ark 客户端
client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key="4185fc5d-ec50-4667-bd93-d42e801fe3de",
)

with open("point_mapping.json", 'r', encoding='utf-8') as f:
        mapping = json.load(f)

mapping_str = json.dumps(mapping, ensure_ascii=False, indent=2)
safe_mapping_str = mapping_str.replace("{", "{{").replace("}", "}}")

def parse_response(text):
    """
    从模型返回文本中提取最后的JSON字符串和前面的推理过程。
    """
    # 用正则匹配最后一个JSON对象，大致思路是匹配从最右边的 { 开始到 } 结束的字符串
    # 这里假设JSON是最后一部分，且单行
    matches = re.findall(r'\{.*\}$', text, re.DOTALL)
    if matches:
        json_str = matches[-1]
        try:
            json_obj = json.loads(json_str)
            cot_text = text[:text.rfind(json_str)].strip()
            return cot_text, json_obj
        except json.JSONDecodeError:
            pass
    # 如果没匹配成功，全部当作cot，json返回空
    return text, {}
fout_cotjsonl = open('output_cot.jsonl', 'w', encoding='utf-8') 

with open('notright_cot.jsonl' , 'r',encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        image_url =data['image_url']
        task_type = data["gt_task_type"]
        point_type = data["gt_point_type"]
        point_name = data["gt_point_name"]
        SYSTEM_PROMPT = """
                        你是汽车“外观”图像分类专家。
                        下面给出了所有合法的二级点位类型(point_type_name)及其对应的三级点位名称(point_name)列表：
                        
                        {mapping_str}
                        
                        请你按照严格的三步推理流程，结合给定的正确答案，生成符合逻辑的推理过程：
                        1. 第一步：确认这是一张“外观”图片，并简要说明依据。
                        2. 第二步：从上述 point_type_name 列表中，选择最符合的那一项，并说明理由。
                        3. 第三步：在选中的 point_type_name 对应的点位名称列表里，选择最符合的 point_name，并说明理由。
                        
                        在推理过程中，请确保你的解释和理由能够合理支持给定的答案。
                        
                        最后，请仅输出一个有效 JSON：
                        {{"task_type":"外观","point_type":"…","point_name":"…","COT":"…"}}
                        且该 JSON 必须与给定的正确答案完全一致。
                        
                        ---
                        【输入图片URL】：{image_url}
                        
                        【正确答案】：
                        {{"task_type": "{task_type}", "point_type": "{point_type}", "point_name": "{point_name}"}}
                        
                        请开始你的推理过程：
                        """         
        safe_mapping_str = mapping_str.replace("{", "{{").replace("}", "}}")
        SYSTEM_PROMPT = SYSTEM_PROMPT.format(
            mapping_str=safe_mapping_str,
            image_url=image_url,
            task_type=task_type,
            point_type=point_type,
            point_name=point_name
        )
        resp = client.chat.completions.create(
                model="doubao-1.5-vision-pro-250328",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            },
                        },
                        {"type": "text", "text":SYSTEM_PROMPT },
                    ],
                }
            ])
        cot = resp.choices[0].message.content.strip()
        cot_text, json_obj = parse_response(cot)
        fout_cotjsonl.write(json.dumps({
            "image_url": image_url,
            "gt_task_type":task_type,
            "gt_point_type": point_type,
            "gt_point_name": point_name,
            "cot": cot_text,
            "model_pred_json": json_obj
        }, ensure_ascii=False) + "\n")
        logging.info(f"成功处理图片: {image_url}")
