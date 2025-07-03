import json
import sys
import requests
from utils import prepare_request
from utils import ak,sk

method = 'POST'
DOMAIN = "api-knowledgebase.mlp.cn-beijing.volces.com"
path = '/api/knowledge/collection/search'

request_params = {
    "name": "zhaopin",
    "project": "",
    "query": "职位的具体工作内容是什么",
    "stream": False,  # 开启流式返回
    "query_param": {},
    "retrieve_param": {
        "rerank_switch": True,
        "retrieve_count": 10,
        "dense_weight": 0.7,
        "limit": 10,
        "chunk_diffusion_count": 1
    },
    "llm_param": {
        "model": "Doubao-pro-32k",
        "max_new_tokens": 2500,
        "min_new_tokens": 5,
        "temperature": 0.8,
        "top_p": 0.95,
        "top_k": 10,
        "prompt": "你是一位在线客服，你的首要任务是通过巧妙的话术回复用户的问题，你需要根据「参考资料」来回答接下来的「用户问题」，这些信息在 <context></context> XML tags 之内.\n\n<context>\n{{.retrieved_chunks}}\n</context>\n\n回答用户的问题，用户的问题在<query></query> XML tags 之内\n回答问题时，你需要根据参考资料给出准确，简洁的回答\n\n<query>\n{{.user_query}}\n</query>",
        "prompt_extra_context": {
            "self_define_fields": ["自定义元数据1", "自定义元数据2"],
            "system_fields": ["doc_name", "title", "chunk_title", "content"]
        }
    }
}

info_req = prepare_request(method = method, path = path, ak = ak, sk = sk,
                           data = request_params)
res = requests.request(method=info_req.method,
                url = "https://{}{}".format(DOMAIN, info_req.path),
                headers = info_req.headers,
                data = info_req.body)
ans = res.json()
for i in ans['data']['result_list']:
    # print(i)
    json_string = i['doc_info']['doc_meta']
    parsed_json = json.loads(json_string)
    for item in parsed_json:
        print(item['field_name'], item['field_value'])

