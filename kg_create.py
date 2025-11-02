import json
import sys
import requests
from utils import prepare_request
from utils import ak,sk

method = 'POST'
DOMAIN = "api-knowledgebase.mlp.cn-beijing.volces.com"
path = '/api/knowledge/collection/create'


request_params = {
    "name": "First_collection",
    "description": "这是一个招聘的数据集",
    "index": {
        "index_type": "hnsw_hybrid",
        "index_config": {
            "fields": [],
            "quant": "int8",
            "cpu_quota": 1,
            "embedding_model": "doubao-embedding-and-m3",
            "embedding_dimension": 2048
        }
    },
    "table_config": {
        "table_type": "row",
        "table_pos": 1,
        "start_pos": 2,
        "table_fields": [
            {
                "field_type": "string",
                "field_name": "问题",
                "if_embedding": True,
                "if_filter": True
            },
            {
                "field_type": "string",
                "field_name": "答案",
                "if_embedding": False,
                "if_filter": False
            }

        ]
    },
    "data_type": "structured_data",
    "project": ""
}

info_req = prepare_request(method = method, path = path, ak = ak, sk = sk,
                           data = request_params)

res = requests.request(method=info_req.method,
                url = "https://{}{}".format(DOMAIN, info_req.path),
                headers = info_req.headers,
                data = info_req.body)

print(res.json())