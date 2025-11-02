import json
import sys
import requests
from utils import prepare_request
from utils import ak,sk

method = 'POST'
DOMAIN = "api-knowledgebase.mlp.cn-beijing.volces.com"
path = '/api/knowledge/point/list'

request_params ={
    "collection_name": "unstructure_Data",
    "project": ""
}

info_req = prepare_request(method = method, path = path, ak = ak, sk = sk,
                           data = request_params)
res = requests.request(method=info_req.method,
                url = "https://{}{}".format(DOMAIN, info_req.path),
                headers = info_req.headers,
                data = info_req.body)
print(res.text)

ans = res.json()
print(ans)
for i in ans['data']['point_list']:
    print(i.keys())
    collection_name = i['collection_name']
    point_id =i['point_id']
    content = i['content']
    chunk_id =i['chunk_id']
    doc_info =i['doc_info']
    doc_id = doc_info['doc_id']
    doc_name = doc_info['doc_name']
    doc_type = doc_info['doc_type']

    chunk_type =i['chunk_type']
    print('point_id',point_id)
    print('content',content)
    print('doc_info', doc_info)
    print('=========')
    print('=========')
    print()
    print()
    print()