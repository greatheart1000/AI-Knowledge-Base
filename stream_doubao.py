#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/3/5 10:45
# @Author  : caijian
# @File    : stream_doubao.py
# @Software: PyCharm
import os
from volcenginesdkarkruntime import Ark

# 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
# 初始化Ark客户端，从环境变量中读取您的API Key
client = Ark(
    # 此为默认路径，您可根据业务所在地域进行配置
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
    api_key="f62bafd2-1269-4169-b072-7994b36541a7",
)



# Streaming:
print("----- streaming request -----")
stream = client.chat.completions.create(
    model="doubao-1-5-pro-32k-250115",
    messages=[
        {"role": "system", "content": "你是人工智能助手."},
        {"role": "user", "content": "常见的十字花科植物有哪些？"},
    ],
    # 响应内容是否流式返回
    stream=True,
)
for chunk in stream:
    if not chunk.choices:
        continue
    print(chunk)
    #print(chunk.choices[0].delta.content, end="")
print()