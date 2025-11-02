import json
import sys
import requests
from utils import prepare_request
from utils import ak,sk

method = 'POST'
DOMAIN = "api-knowledgebase.mlp.cn-beijing.volces.com"
path = '/api/knowledge/doc/update_meta'

request_params = {
    "collection_name": "unstructure_Data",
    "project": "",
    "doc_id": "pdf_zhaopin",
    "meta":[
    {"field_name":"category","field_type":"string", "field_value":"招聘"},
    {"field_name":"是否公开","field_type":"bool", "field_value":True},
    ]
}

info_req = prepare_request(method = method, path = path, ak = ak, sk = sk,
                           data = request_params)
res = requests.request(method=info_req.method,
                url = "https://{}{}".format(DOMAIN, info_req.path),
                headers = info_req.headers,
                data = info_req.body)
print(res.json())
