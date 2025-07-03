import json
import sys
import requests
from utils import prepare_request
from utils import ak,sk

method = 'POST'
DOMAIN = "api-knowledgebase.mlp.cn-beijing.volces.com"
path = '/api/knowledge/collection/create'


request_params = {
    "name": "unStructured_Knowledge",
    "description": "这是一个非结构性文档集合",
    "index": {
        "index_type": "hnsw_hybrid",
        "index_config": {
            "fields": [{"field_name": "category", # 自定义标量字段，用于区分文档领域
                       "field_type": "string"}],
            "quant": "int8",
            "cpu_quota": 1,
            "embedding_model": "doubao-embedding-and-m3",
            "embedding_dimension": 2048}
    },
    "data_type": "unstructured_data",
    "preprocessing":{
                "chunking_strategy":"custom_balance",
                "chunk_length":500,
                "merge_small_chunks":True,
                "multi_modal":["image_ocr"]
                },
    "project": "default",
}
info_req = prepare_request(method = method, path = path, ak = ak, sk = sk,
                           data = request_params)
res = requests.request(method=info_req.method,
                url = "https://{}{}".format(DOMAIN, info_req.path),
                headers = info_req.headers,
                data = info_req.body)
print(res.json())
