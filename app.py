import random
from flask import Flask, request
from flask import jsonify
import os
import json
from dashvector import Client, Doc
import requests
import numpy as np
import time
from utils import prepare_request,ak ,sk,method ,DOMAIN
from logger import get_logger
logger = get_logger(log_file="log.txt")
logger.info("在吗")
logger.info('merged_lora_path')

app = Flask(__name__)

def remove_stop_words(text):
    # 定义停用词
    if len(text)==1:
        return text
    stop_words = ['.','。','。', '!', '！', '呀', '呢', '~', ' ','，',',','?','？','？']
    for stop_word in stop_words:
        text = text.replace(stop_word, '')
    if len(text)>2 and text.endswith("了"):
        text = text[:-1]
    if len(text)>2 and text.endswith("啊"):
        text = text[:-1]
    if len(text)>2 and text.endswith("的"):
        text = text[:-1]
    return text




@app.route('/create_collection', methods=['POST'])
def create_collection():
    try:
        logger.info(f"=====create collection用于创建一个新的知识库。创建成功后，可以导入数据=====")
        path = '/api/knowledge/collection/create'
        data = request.get_json()  # 从POST请求中获取数据
        name = data['name']
        description = data['description']
        data_type =data['data_type'] # 0 structured_data 1: unstructured_data
        if data_type==0:
            request_params = {
                "name": name,
                "description": description,
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
                "project": "default"
            }
            info_req =prepare_request(method = method, path = path, ak = ak, sk = sk,
                           data = request_params)
            res = requests.request(method=info_req.method,
                                   url="https://{}{}".format(DOMAIN, info_req.path),
                                   headers=info_req.headers,
                                   data=info_req.body)
            print(res.text)
        else:
            request_params = {
                "name": name,
                "description": description,
                "index": {
                    "index_type": "hnsw_hybrid",
                    "index_config": {
                        "fields": [],
                        "quant": "int8",
                        "cpu_quota": 1,
                        "embedding_model": "doubao-embedding-and-m3",
                        "embedding_dimension": 2048}
                },
                "data_type": "unstructured_data",
                "preprocessing": {
                    "chunking_strategy": "custom_balance",
                    "chunk_length": 500,
                    "merge_small_chunks": True,
                    "multi_modal": ["image_ocr"]
                },
                "project": "default",
            }
            info_req = prepare_request(method=method, path=path, ak=ak, sk=sk,
                                       data=request_params)
            res = requests.request(method=info_req.method,
                                   url="https://{}{}".format(DOMAIN, info_req.path),
                                   headers=info_req.headers,
                                   data=info_req.body)
            print(res.text)
    except Exception as e:
        return jsonify({'message': 'batch insert data failed', 'status_code': 300})


@app.route('/doc_add', methods=['POST'])
def doc_add():
    try:
        logger.info(f"=====用于向已创建的知识库导入文档=====")
        path = '/api/knowledge/doc/add'
        data = request.get_json()  # 从POST请求中获取数据
        name = data['name']
        doc_id = data['doc_id']
        doc_name = data['doc_name']
        doc_type =data['doc_type']
        url = data['url']
        request_params = {
            "collection_name": name ,
            "project": "",
            "add_type": "url",
            "doc_id":doc_id,
            "doc_name": doc_name,
            "doc_type": doc_type,
            "url": url,
            "meta": [
                {"field_name": "问题", "field_type": "string", "field_value": "这个职位的具体工作内容是什么？"},
                {"field_name": "答案", "field_type": "string", "field_value": "作为软件工程师，您将负责开发、测试和维护我们的软件产品。"}
            ]
        }
        info_req = prepare_request(method=method, path=path, ak=ak, sk=sk, data=request_params)
        res = requests.request(method=info_req.method,
                               url="https://{}{}".format(DOMAIN, info_req.path),
                               headers=info_req.headers,
                               data=info_req.body)
        print(res.text)
    except Exception as e:
        return jsonify({'message': 'doc  add data failed', 'status_code': 300})






