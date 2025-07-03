import json
import sys
import requests
from utils import prepare_request
from utils import ak, sk

method = 'POST'
DOMAIN = "api-knowledgebase.mlp.cn-beijing.volces.com"
path = '/api/knowledge/collection/search'

# 修改查询字段为 '问题'
request_params = {
    "name": "unstructure_Data",
    "project": "",
    "query": "这个职位的底薪是多少？",
    "retrieve_count": 5,
    "limit": 2,
    "query_param": {
        "doc_filter": {
            "op": "must",
            "field": "category",  # 修改为 '问题'
            "conds": ["这个职位的底薪是多少？"]  # 你要过滤的具体问题
        },
    },
    "rerank_switch": True,
    "dense_weight": 0.5
}

info_req = prepare_request(method=method, path=path, ak=ak, sk=sk, data=request_params)
res = requests.request(method=info_req.method,
                       url="https://{}{}".format(DOMAIN, info_req.path),
                       headers=info_req.headers,
                       data=info_req.body)
print(res.text)