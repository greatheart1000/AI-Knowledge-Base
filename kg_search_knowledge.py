import json
import requests
from utils import prepare_request
from utils import ak, sk

method = 'POST'
DOMAIN = "api-knowledgebase.mlp.cn-beijing.volces.com"
path = '/api/knowledge/collection/search_knowledge'

request_params = {
    "name": "unstructure_Data",
    "query": "职位的底薪是多少？",
    "limit": 5,
    "query_param": {},
    "dense_weight": 0.5,
    "pre_processing": {
        "need_instruction": True,
        "rewrite": True,
        "messages": [
            {
                "role": "system",
                "content": "你是一个智能助手，帮助用户回答招聘相关的问题。"
            },
            {
                "role": "user",
                "content": "我想了解这个职位的薪资情况。"
            },
            {
                "role": "assistant",
                "content": "这个职位的薪资包括底薪和绩效。你想具体了解哪一部分？"
            },
            {
                "role": "user",
                "content": "我想知道职位的底薪是多少。"
            }
        ],
        "return_token_usage": True
    },
    "post_processing": {
        "rerank_switch": False,
        "rerank_model": "Doubao-pro-4k-rerank",
        "rerank_only_chunk": False,
        "retrieve_count": 5,
        "endpoint_id": "ep",
        "chunk_group": False,
        "get_attachment_link": False
    }
}
info_req = prepare_request(method=method, path=path, ak=ak, sk=sk, data=request_params)
res = requests.request(
    method=info_req.method,
    url="https://{}{}".format(DOMAIN, info_req.path),
    headers=info_req.headers,
    data=info_req.body
)
print(res.text)
ans = res.json()

for i in ans['data']["result_list"]:
    print(i)