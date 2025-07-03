import json
import sys
import requests
from utils import prepare_request
from utils import ak,sk

method = 'POST'
DOMAIN = "api-knowledgebase.mlp.cn-beijing.volces.com"
path = '/api/knowledge/collection/update'

request_params = {
    "name": "apiexample",
    "project": "",
    "description": "这是一个测试的知识库",
    "cpu_quota": 1
}
info_req = prepare_request(method = method, path = path, ak = ak, sk = sk,
                           data = request_params)
res = requests.request(method=info_req.method,
                url = "https://{}{}".format(DOMAIN, info_req.path),
                headers = info_req.headers,
                data = info_req.body)

print(res.text)