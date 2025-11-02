#coding:utf-8
TRIPLET_EXTRACT_PT = """
请从以下文本中提取所有三元组。每个三元组应包含一个主体（Subject）、一个谓词（Predicate）和一个宾语（Object），并准确反映文本中的关系或事实。忽略无关的背景信息或修饰语。

请按照以下格式回答：
(主体, 谓词, 宾语)

context：
"阿里巴巴集团宣布与蚂蚁金服合作，共同开发新技术，以提升用户支付体验。"

示例：
(阿里巴巴集团, 宣布, 与蚂蚁金服合作)
(阿里巴巴集团, 开发, 新技术)
(新技术, 提升, 用户支付体验)

现在请你根据提供的文本，遵循限制来输出所有的三元组。
<context>
输出所有的三元组:

"""
import json
import sys
import requests
from utils import prepare_request
from utils import ak,sk

method = 'POST'
DOMAIN = "api-knowledgebase.mlp.cn-beijing.volces.com"
path = '/api/knowledge/chat/completions'

query="""字节大模型外包岗位职位序列：图像算法训练师、数据标注专员——随着大模型的发展，对人选的技术能力要求可能会发生哪些变化？如何提前准备？
随着大模型的不断发展，技术能力要求可能会发生以下变化：

1. 对图像算法训练师的要求变化：
更强的多模态能力：未来将要求图像算法训练师具备处理多模态数据的能力，不仅是图像，还包括图像与文本、语音等的融合。
深度学习框架的掌握：对如PyTorch、TensorFlow等框架的掌握会变得更加重要，特别是对模型的调优和优化。
预训练模型的使用与微调：未来可能更多地依赖预训练的视觉模型（如ViT、CLIP），要求训练师具备如何微调这些大模型的能力。
2. 对数据标注专员的要求变化：
高质量数据标注：随着大模型的发展，数据标注的质量要求会越来越高，标注专员需要具备一定的领域知识，以便提供更精准的标注。
自动化标注工具的使用：未来可能会更多使用自动化标注工具，标注专员需要学习如何与这些工具配合工作，提高标注效率。
提前准备的方向：
强化深度学习知识：无论是图像算法训练师还是数据标注专员，未来都需要更深的机器学习/深度学习知识。
掌握多模态技术：随着多模态AI的发展，掌握如何处理、融合多种数据（图像、语音、文本）将成为重要的技术能力。
提升自动化标注工具的使用能力：学习如何使用数据标注中的自动化工具，如Active Learning、半自动标注等，将有助于提高工作效率。"""

input = TRIPLET_EXTRACT_PT.replace('<context>',query)

request_params = {
    "model": "Doubao-lite-4k",
    "max_tokens": 4096,
    "temperature": 0.1,
    "messages": [
        {"role": "system", "content": "你是一个智能助手。"},
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好！有什么我可以帮助你的？"},
        {"role": "user", "content": input},
    ],
    "stream": False,
    "return_token_usage": True
}
info_req = prepare_request(method = method, path = path, ak = ak, sk = sk,
                           data = request_params)
res = requests.request(method=info_req.method,
                url = "https://{}{}".format(DOMAIN, info_req.path),
                headers = info_req.headers,
                data = info_req.body)
print(res.json()['data']['generated_answer'])
