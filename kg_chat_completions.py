import json
import sys
import requests
from utils import prepare_request
from utils import ak,sk

method = 'POST'
DOMAIN = "api-knowledgebase.mlp.cn-beijing.volces.com"
path = '/api/knowledge/chat/completions'

request_params = {
    "model": "Doubao-lite-4k",
    "max_tokens": 4096,
    "temperature": 0.1,
    "messages": [
        {"role": "system", "content": "你是一个智能助手。"},
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好！有什么我可以帮助你的？"},
        {"role": "user", "content": "请你生成一个提取三元组的prompt"},
    ],
    "stream":True,
    "return_token_usage": True
}
info_req = prepare_request(method = method, path = path, ak = ak, sk = sk,
                           data = request_params)
res = requests.request(method=info_req.method,
                url = "https://{}{}".format(DOMAIN, info_req.path),
                headers = info_req.headers,
                data = info_req.body)
print(res.text)