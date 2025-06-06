vllm serve /root/autodl-tmp/Qwen2.5-VL-7B-Instruct-merged --limit-mm-per-prompt image=4 
https://www.aivi.fyi/llms/deploy-Qwen2.5-VL

https://gitcode.com/gh_mirrors/swift1/swift/blob/main/examples/infer/vllm/mllm_tp.sh


import requests
import base64
from openai import OpenAI
import json

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

with open("point_mapping.json", 'r', encoding='utf-8') as f:
    mapping = json.load(f)

mapping_str = json.dumps(mapping, ensure_ascii=False, indent=2)

SYSTEM_PROMPT = f"""
你是汽车图像分类专家。
下面给出了所有合法的二级点位类型(point_type_name) (辅助图,整体外观,其他细节)及其对应的三级点位名称(point_name)列表：
{mapping_str}
请你按照严格的三步推理流程，结合给定的图片，生成符合逻辑的推理过程：
1. 第一步：确认这是一张“外观”图片，并简要说明依据。
2. 第二步：从上述 point_type_name 列表中，选择最符合的那一项，并说明理由。
3. 第三步：在选中的 point_type_name 对应的点位名称列表里，选择最符合的 point_name，并说明理由。

在推理过程中，请确保你的解释和理由能够合理支持给定的答案。

最后，请仅输出一个有效 JSON：
{{"task_type": "外观", "point_type": "…", "point_name": "…"}}
请开始你的推理过程：
"""

import requests
import base64

# # 定义请求 URL
# url = "http://localhost:8000/v1/chat/completions"

# # 定义请求头
# headers = {
#     "Content-Type": "application/json"
# }

# # 图片路径
# image_path = "f2b2c190-e4a2-466a-b9bf-6578e4e4d9b0.jpg"

# # 编码图片为 Base64
# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode('utf-8')

# base64_image = encode_image(image_path)

# # 定义请求体
# data = {
#     "model": "/root/autodl-tmp/Qwen2.5-VL-7B-Instruct-merged",
#     "messages": [
#         {
#             "role": "user",
#             "content": [
#                 {"type": "text", "text": SYSTEM_PROMPT},
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": f"data:image/jpeg;base64,{base64_image}",
#                     },
#                 },
#             ]
#         }
#     ],
#     "max_tokens": 1024,
# }

# # 发送 POST 请求
# response = requests.post(url, headers=headers, json=data)

# # 打印响应
# if response.status_code == 200:
#     print("响应成功:")
#     print(response.json())
# else:
#     print(f"请求失败，状态码: {response.status_code}")
#     print(response.text)
