# -*- coding: utf-8 -*-
import requests
import numpy as np
import time
from logger import get_logger
from flask import Flask, request,jsonify,Response
import os
import json
import random
from json.decoder import JSONDecodeError
from datetime import datetime
from logger import get_logger
from utils import prepare_request,ak ,sk,method ,DOMAIN,remove_stop_words,base_prompt,generate_prompt
import re
from utils import chat_completion
from volcengine.viking_knowledgebase import VikingKnowledgeBaseService
from graph_prompt import relationship_prompt
import pymysql
import aiohttp
import asyncio
from utils import insert_list_to_mysql
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
logger = get_logger(log_file="log.txt",file_mode ='a')
viking_knowledgebase_service = VikingKnowledgeBaseService(
    host="api-knowledgebase.mlp.cn-beijing.volces.com",
    scheme="https", connection_timeout=30, socket_timeout=30)
viking_knowledgebase_service.set_ak(ak)
viking_knowledgebase_service.set_sk(sk)
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 确保 JSON 不转义非 ASCII 字符
app.config['JSONIFY_MIMETYPE'] = 'application/json;charset=utf-8'  # 设置 JSON MIME包含 charset=utf-8

logger.info(f"===AI knowledge_Base project is running  ===")


@app.route('/create_collection', methods=['POST'])
def create_collection():
    try:
        logger.info(f"=====create collection用于创建一个新的知识库,可以导入数据=====")
        path = '/api/knowledge/collection/create'
        data = request.get_json()  # 从POST请求中获取数据
        print('data:',data)
        name = data['name']
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]{0,63}$'
        if not re.match(pattern, name):
            logger.info(" 创建知识库失败,知识库的名字只能使用英文字母、数字、下划线_，并以英文字母开头不能为空")
            result ={"message":"创建知识库失败,知识库的名字只能使用英文字母、数字、下划线_,并以英文字母开头,不能为空","timestamp":timestamp,'status_code': 300}
            print(result)
            return jsonify(result)
        description = data['description']
        # 0 structured_data 1: unstructured_data
        data_type = int(data['data_type'])
        length = data.get('length', None)
        length =int(length)
        fields =  []
        tags =data.get('tags', None)
        if tags is not None:
            for key, value in tags.items():
                print(f"{key}: {value}")
                fields.append({"field_name": key, 
                               "field_type": "string",
                               "field_value":value})  
        print('name:',name,'description:',description,'length:',length)
        if data_type==0:
            logger.info(f"=== create structure collection ===")
            request_params = {
                "name": name,
                "description": description,
                    "index": {
                    "index_type": "hnsw_hybrid",
                    "index_config": {
                        "fields": fields,
                        "quant": "int8",
                        "cpu_quota": 1,
                        "embedding_model": "doubao-embedding-and-m3",
                        "embedding_dimension": 2048}
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
            code =res.json()['code']
            if code==0:
                logger.info(" === create structure collection suceess === ")
                result ={"message":"create structure collection suceess",
                         "timestamp":timestamp,'status_code': 200}
                return jsonify(result)
            else:
                logger.info(" === create structure collection failed  === ")
                result ={"message":"create structure collection failed",
                         "timestamp":timestamp,'status_code': 300}
                return jsonify(result)
        else:
            logger.info(f" === create unstructured collection === ")
            request_params = {
                "name": name,
                "description": description,
                "index": {
                    "index_type": "hnsw_hybrid",
                    "index_config": {
                        "fields": fields,
                        "quant": "int8",
                        "cpu_quota": 1,
                        "embedding_model": "doubao-embedding-and-m3",
                        "embedding_dimension": 2048}
                        },
                "data_type": "unstructured_data",
                "preprocessing": {
                    "chunking_strategy": "custom_balance",
                    "chunk_length": length,
                    "merge_small_chunks": True,
                    "multi_modal": ["image_ocr"] },
                "project": "default",
                }
            info_req = prepare_request(method=method, path=path, ak=ak, sk=sk,
                                       data=request_params)
            res = requests.request(method=info_req.method,
                                   url="https://{}{}".format(DOMAIN, info_req.path),
                                   headers=info_req.headers,
                                   data=info_req.body)
            ans =res.json()
            print('ans:',ans)
            code =ans['code']
            message = ans['message']
            if code==0:
                
                result ={"message":f"create unstructured collection {name} suceess",
                         "timestamp":timestamp,'status_code': 200}
                logger.info(f"create unstructured collection {name} suceess ")
                return jsonify(result)
            else:
                message = res.json()['message']
                logger.info(f"create unstructured collection {name} failed, message :{message}")
                result ={"message":f"create unstructured collection {name} failed, message : {message}",  "timestamp":timestamp,'status_code': 200}
                return jsonify(result)

    except Exception as e1:
        print(e1)
        return jsonify({'message': f'create collection failed,{e1}', 'status_code': 300})


@app.route('/collection_info', methods=['POST'])
def collection_info():
    try:
        logger.info(f"===collection_info接口用于查询指定数据集 的详情信息=====")
        path = '/api/knowledge/collection/info'
        data = request.get_json()  # 从POST请求中获取数据
        print('data',data)
        name = data['name']
        request_params = {
                "name": name,
                "project": ""
                        }
        info_req = prepare_request(method = method, path = path, ak = ak, sk = sk, data = request_params)
        res = requests.request(method=info_req.method,
                url = "https://{}{}".format(DOMAIN, info_req.path),
                headers = info_req.headers,
                data = info_req.body)
        ans  = res.json()
        code = ans['code']
        if code == 0:
            #print('collection: ',ans['data'])
            point_num = ans['data']['pipeline_list'][0]['pipeline_stat']['point_num']
            collection_name = ans['data']['collection_name']
            description   = ans['data']['description']
            create_time = ans['data']['create_time']
            update_time = ans['data']['update_time']
            # 将时间戳转换为datetime对象
            create_time_dt = datetime.fromtimestamp(create_time)
            update_time_dt = datetime.fromtimestamp(update_time)
            create_time_formatted = create_time_dt.strftime('%Y-%m-%d %H:%M:%S')
            update_time_formatted = update_time_dt.strftime('%Y-%m-%d %H:%M:%S')
            #print('preprocessing_list', ans['data']['pipeline_list'])
            data_type =ans['data']['pipeline_list'][0]['data_type']
            #print('data_type',data_type)
            fileds  = ans['data']['pipeline_list'][0]['index_list'][0]['index_config']
            #print('fileds',fileds)
            #for i in fileds:
            #    print(i)
            #embedding_model = ans['data']['embedding_model']
            #embedding_dimension = ans['data']['embedding_dimension']
            msg ={"collection_name":collection_name,
                  "description":description,
                  "create_time":create_time_formatted,
                  "update_time":update_time_formatted,
                  "data_type"  :data_type,
                  "point_num" :point_num,
                  **({"doc_num": ans['data']['doc_num']} if 'doc_num' in ans['data'] else {})
                  }
            result ={"message":msg,"timestamp":timestamp ,'status_code': 200}
            logger.info(f"{result}")
            return jsonify(result)
        else:
            message = ans['message']
            logger.info(f"collection info  {name}  failed, message : {message}")
            result = {"message":f"collection info {name}  failed , message: {message}","timestamp":timestamp,'status_code': 200}
            return jsonify(result)
    except Exception as e:
        print(e)
        logger.error(f"Error in collection info: {e}")
        return jsonify({'message': f'{e}', 'status_code': 300})



@app.route('/list_collections', methods=['POST'])
def list_collections():
    try:
        logger.info(f"=====list_collection用于列出所有的知识库Collection =====")
        data =[]
        my_collection = viking_knowledgebase_service.list_collections()
        for collection in my_collection:
            collection_name = collection.collection_name
            description = collection.description
            project = collection.project
            create_time = collection.create_time
            dt_object = datetime.fromtimestamp(create_time)
            readable_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
            doc_num = collection.doc_num
            data.append({"collection_name":collection_name,"description":description,"project":project,"create_time":readable_time,"doc_num":doc_num})
        sorted_data = sorted(data, key=lambda x: x["create_time"], reverse=True)

        logger.info(f"list_collections  success")

        print()
        result ={"result":sorted_data,'status_code': 200}
        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({'message': 'get list_collections failed', 'status_code': 300})


@app.route('/update_collection', methods=['POST'])
def update_collection():
    try:
        logger.info(f"===== update_collection用于更新已有的指定知识库Collection配置 =====")
        data = request.get_json()  # 从POST请求中获取数据
        name =data['name']
        description =data['description']
        my_collection = viking_knowledgebase_service.update_collection(name, description=description, cpu_quota=1)
        print(my_collection)
        result = {"result":"update_collection success",'status_code': 200}
        logger.info(f"{result}")
        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({'message': 'update_collection  failed', 'status_code': 300})



@app.route('/add_doc', methods=['POST'])
def add_doc():
    try:
        logger.info(f"=====用于向已创建的知识库导入文档=====")
        path = '/api/knowledge/doc/add'
        data = request.get_json()  # 从POST请求中获取数据
        print('data:' ,data)

        name     = data['name']
        doc_id   = data['doc_id']
        doc_name = data['doc_name']
        doc_type = data['doc_type']
        url      = data['url']
        meta = data['meta']
        request_params = {
                        "collection_name": name ,
                        "project": "",
                        "add_type": "url",
                        "doc_id":doc_id,
                        "doc_name": doc_name,
                        "doc_type": doc_type,
                        "url": url,
                        "meta": meta
                        }

        info_req = prepare_request(method=method, path=path, ak=ak, sk=sk, data=request_params)
        res = requests.request(method=info_req.method,
                               url="https://{}{}".format(DOMAIN, info_req.path),
                               headers=info_req.headers,
                               data=info_req.body)
        ans = res.json()
        code= ans['code']
        if code == 0:
            result ={"message":f"add doc {doc_name} to {name} collection success ","timestamp":timestamp ,'status_code': 200}
            return jsonify(result)
        else:
            message = ans['message']
            logger.info(f"add doc failed, message : {message}")
            result = {"message":f"add doc {doc_name} to {name} collection  failed , message: {message}","timestamp":timestamp,'status_code': 300}
            return jsonify(result)
    except Exception as e:
        #logger.error(f"Error in doc_add: {e}")
        return jsonify({'message': f'{e}', 'status_code': 300})

@app.route('/get_doc', methods=['POST'])
def get_doc():
    try:
        logger.info(f"===== 用于查看知识库下的某个文档的信息 =====")
        data = request.get_json()  # 从POST请求中获取数据
        name = data['name']
        doc_id  = data['doc_id']
        collection = viking_knowledgebase_service.get_collection( name )
        doc = collection.get_doc(doc_id)
        collection_name = doc.collection_name
        point_num = doc.point_num
        doc_name = doc.doc_name
        url   = doc.url
        result = {
                "collection_name":collection_name,"doc_id":doc_id,"doc_name":doc_name ,
                "point_num":point_num,"url":url,'status_code': 200
                 }
        logger.info(f"get doc success , result : {result}")
        print()
        return jsonify(result)

    except Exception as e1:
        logger.error(f"Error in get doc: {e1}")
        return jsonify({'message': f'get doc failed,{e1}', 'status_code': 300})


@app.route('/list_docs', methods=['POST'])
def list_docs():
    try:
        # https://www.volcengine.com/docs/84313/1269161
        logger.info(f"===== 用于list_docs用于查看某个知识库下的文档")
        path = '/api/knowledge/doc/list'
        data = request.get_json()  # 从POST请求中获取数据
        name = data['name']
        request_params ={ "collection_name": name, "project": ""}
        info_req = prepare_request(method = method, path = path, ak = ak, sk = sk,
                           data = request_params)
        res = requests.request(method=info_req.method,
                url = "https://{}{}".format(DOMAIN, info_req.path),
                headers = info_req.headers,
                data = info_req.body)
        result = []
        ans = res.json()
        code =ans['code']
        if code == 0:
            #print(ans)
            total_num = ans['data']['total_num']
            count =ans['data']['count']
            doc_list = ans['data']['doc_list']
            #print(doc_list)
            for i in doc_list:
                #print(i)
                print('==========')
                doc_name = i['doc_name']
                doc_id = i['doc_id']
                doc_type = i['doc_type']
                create_time = i['create_time']
                dt_object = datetime.fromtimestamp(create_time)
                readable_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                update_time = i['update_time']
                up_object = datetime.fromtimestamp(update_time)
                up_readable_time = up_object.strftime('%Y-%m-%d %H:%M:%S')
                status = i['status']
                process_status = status['process_status']
                res = {"doc_name":doc_name,"doc_id":doc_id,"doc_type":doc_type,"create_time":readable_time,"update_time":up_readable_time,"process_status":process_status}
                result.append(res)
            print(result)
            result = sorted(result, key=lambda x: x['update_time'], reverse=True)
            return jsonify(result)
        else:
            message = ans['message']
            logger.info(f"list_docs failed ,message :{message}")
            result = {"message":f" list_docs failed , message: {message}","timestamp" : timestamp,'status_code': 300}
            return jsonify(result)

    except Exception as e1:
        print(e1)
        return jsonify({'message':f'get list_docs failed , {e1}', 'status_code': 300})




@app.route('/list_points', methods=['POST'])
def list_points():
    try:
        # https://www.volcengine.com/docs/84313/1269161
        logger.info(f"===== 用于list_points用于查看某个知识库下的知识点信息")
        path = '/api/knowledge/point/list'
        data = request.get_json()  # 从POST请求中获取数据
        name = data['name']
        request_params ={ "collection_name": name, "project": ""}
        info_req = prepare_request(method = method, path = path, ak = ak, sk = sk,
                           data = request_params)
        res = requests.request(method=info_req.method,
                url = "https://{}{}".format(DOMAIN, info_req.path),
                headers = info_req.headers,
                data = info_req.body)
        result = []
        contents = []
        ans = res.json()
        code =ans['code']
        if code == 0:
            total_num = ans['data']['total_num']
            res = ans['data']['point_list'][0]
            chunk_type = res['chunk_type']
            if chunk_type == 'structured':
                for i in ans['data']['point_list']:
                    #print(i)
                    point_id = i['point_id']
                    content  = i['content']
                    chunk_id = i['chunk_id']
                    doc_id = i['doc_info']['doc_id']
                    doc_name= i['doc_info']['doc_name']
                    doc_type = i['doc_info']['doc_type']
                    doc_meta = i['doc_info']['doc_meta']
                    update_time = i['update_time']
                    dt_object = datetime.fromtimestamp(update_time)
                    update_time  = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                    table_chunk_fields = i.get('table_chunk_fields', [])
                    for field in table_chunk_fields:
                        if field['field_name'] == "问题":
                            question = field['field_value']
                        elif field['field_name'] == "答案":
                            answer = field['field_value']
                    msg =   {
                            "point_id":point_id,
                            "question":question,
                            "answer":answer,
                            "chunk_id":chunk_id,
                            "doc_id":doc_id,
                            "doc_name":doc_name,
                            "update_time":update_time,
                            "doc_type":doc_type,
                            "doc_meta":doc_meta

                         }
                    contents.append(msg)
            else:
                chunk_type = "unstructured"
                for i in ans['data']['point_list']:
                    #print(i)
                    update_time = i['update_time']
                    dt_object = datetime.fromtimestamp(update_time)
                    update_time  = dt_object.strftime('%Y-%m-%d %H:%M:%S')

                    point_id = i['point_id']
                    content  = i['content']
                    chunk_id = i['chunk_id']
                    doc_id = i['doc_info']['doc_id']
                    doc_name= i['doc_info']['doc_name']
                    doc_type = i['doc_info']['doc_type']
                    doc_meta = i['doc_info']['doc_meta']
                    msg =   {
                            "point_id":point_id,
                            "content":content,
                            "chunk_id":chunk_id,
                            "doc_id":doc_id,
                            "doc_name":doc_name,
                            "update_time":update_time,
                            "doc_type":doc_type,
                            "doc_meta":doc_meta
                         }
                    contents.append(msg)
            result ={
                "total_num" : total_num ,
                "chunk_type":chunk_type,
                "contents":contents
                    }
            print('result: ' ,result)
            return jsonify(result)
        else:
            message = ans['message']
            logger.info(f"list_points failed ,message :{message}")
            result = {"message":f" list_points failed , message: {message}","timestamp" : timestamp,'status_code': 300}
            return jsonify(result)

    except Exception as e1:
        print(e1)
        return jsonify({'message':f'get list_points failed , {e1}', 'status_code': 300})


@app.route('/fetch_point', methods=['POST'])
def fetch_point():
    try:
        # https://www.volcengine.com/docs/84313/1269161
        logger.info(f"===== fetch_point 用于从知识库查询所有切片 ====")
        path = '/api/knowledge/doc/list'
        data = request.get_json()  # 从POST请求中获取数据
        print('data:',data)
        name = data['name']
        response = requests.post(url="http://localhost:5000/collection_info",
                                 json= {"name":name})
        # print("----------",response.json()['message']['data_type'])
        data_type = response.json()['message']['data_type']
        print("data_type",data_type)
        """1.首先获取其中类型"""
        request_params ={
            "collection_name": name,
            "project": ""
                        }
        info_req = prepare_request(method = method, path = path, ak = ak, sk = sk,
                           data = request_params)
        res = requests.request(method=info_req.method,
                url = "https://{}{}".format(DOMAIN, info_req.path),
                headers = info_req.headers,
                data = info_req.body)
        ans = res.json()
        result_list = []
        if ans['code']==0:
            #print("doc_list",len(ans['data']['doc_list']))
            logger.info(f" fetch doc_lists from collection {name} success  ")
            #print("===ans===",ans['data'])
            if 'doc_list' not in ans['data']:
                return jsonify({"result" : result_list})
            for i in ans['data']['doc_list']:
                point_num = i['point_num']
                process_status = i['status']['process_status']
                if process_status!=0 and point_num==0:
                    continue
                else:
                    doc_name =i['doc_name']
                    doc_id = i['doc_id']
                    doc_type = i['doc_type']
                    point_num = i['point_num']
                    print(f"======doc_name:{doc_name} point_num:{point_num}")
                    nums = (point_num//100+1)
                    for num in range(nums):
                        print("offset:" ,num*100)
                        point_path = '/api/knowledge/point/list'
                        data = request.get_json()  # 从POST请求中获取数据
                        point_request_params = {
                                "collection_name": name,
                                "project": "",
                                "limit":100,
                                "doc_ids":[doc_id],
                                "offset":num*100 }
                        info_req = prepare_request(method = method, path = point_path,
                        ak = ak, sk = sk,data = point_request_params)
                        point_res =  requests.request(
                            method=info_req.method,
                            url = "https://{}{}".format(DOMAIN, info_req.path),
                            headers = info_req.headers,
                            data = info_req.body  )
                        point_ans = point_res.json()
                        #print(point_ans['data'])
                        point_list = point_ans['data']['point_list']
                        print(f'第{num+1}次获得的知识切片: ',len(point_list))
                        for point in point_list:
                            if data_type == "structured_data":
                                #print(point)
                                point_id = point['point_id']
                                chunk_id = point['chunk_id']
                                table_chunk_fields = point['table_chunk_fields']
                                for field in table_chunk_fields:
                                    if field['field_name'] == "问题":
                                        question = field['field_value']
                                    elif field['field_name'] == "答案":
                                        answer = field['field_value']
                                doc_name = point['doc_info']['doc_name']
                                doc_type =point['doc_info']['doc_type']
                                create_time = point['doc_info']['create_time']
                                update_time = point['update_time']
                                dt_object = datetime.fromtimestamp(update_time)
                                update_time  = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                                result ={
                                    "point_id":point_id,
                                    "chunk_id":chunk_id,
                                    "question":question,
                                    "answer":answer,
                                    "doc_name":doc_name,
                                    "doc_type":doc_type,
                                    "create_time":create_time,
                                    "update_time":update_time,
                                        }
                                result_list.append( result)
                                #print("*************")
                            else:
                                #print(point)
                                #print("*************")
                                point_id = point['point_id']
                                chunk_id = point['chunk_id']
                                content =point['content']
                                doc_id = point['doc_info']['doc_id']
                                doc_name = point['doc_info']['doc_name']
                                doc_type =point['doc_info']['doc_type']
                                create_time = point['doc_info']['create_time']
                                dt_object = datetime.fromtimestamp(create_time)
                                create_time  = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                                update_time = point['update_time']
                                dt_object = datetime.fromtimestamp(update_time)
                                update_time  = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                                if 'chunk_title' in point:
                                    chunk_title = point['chunk_title']
                                    result ={
                                        "point_id":point_id,
                                        "chunk_id":chunk_id,
                                        "content":content,
                                        "chunk_title":chunk_title,
                                        "doc_id":doc_id,
                                        "doc_name":doc_name,
                                        "doc_type":doc_type,
                                        "create_time":create_time,
                                        "update_time":update_time,
                                        }
                                else:
                                    result ={
                                        "point_id":point_id,
                                        "chunk_id":chunk_id,
                                        "content":content,
                                        "doc_id":doc_id,
                                        "doc_name":doc_name,
                                        "doc_type":doc_type,
                                        "create_time":create_time,
                                        "update_time":update_time,
                                    }
                                result_list.append( result)
                    print("====")
                    print("====")
                    print()
                    print()
                    #for j in point_ans['data']:
                    #    print(j)
                    #    print("====")
                    #    print()
                result = []
                print('总切片数量:',len(result_list))
            return jsonify({"result" : result_list})
        else:
            message = ans['message']
            logger.info(f" fetch docs from collection {name} failed ,message : {message}  ")
            result = {"message":f" {message} ","timestamp" : timestamp,'status_code': 300}
            return jsonify(result)
    except Exception as e1:
        print(e1)
        return jsonify({'message': f'fetch point failed,{e1}', 'status_code': 300})



@app.route('/delete_point', methods=['POST'])
def delete_point():
    try:
        # https://www.volcengine.com/docs/84313/1269161
        logger.info(f"===== delete_point 用于从知识库删除一个知识库下的某个切片 ====")
        path = '/api/knowledge/point/delete'
        data = request.get_json()  # 从POST请求中获取数据
        print('data:',data)
        name = data['name']
        point_id = data['point_id']
        request_params ={
            "collection_name": name,
            "project": "",
            "point_id":point_id
                        }
        # collection22  unstructure_Data
        info_req = prepare_request(method = method, path = path, ak = ak, sk = sk,
                           data = request_params)
        res = requests.request(method=info_req.method,
                url = "https://{}{}".format(DOMAIN, info_req.path),
                headers = info_req.headers,
                data = info_req.body)
        ans = res.json()
        if ans['code']==0:
            logger.info(f" delete {point_id} from collection {name} success  ")
            result = {"message":f" delete {point_id} from collection {name} success ","timestamp" : timestamp ,'status_code': 200}
            return jsonify(result)
        else:
            message = ans['message']
            logger.info(f" delete {point_id} from collection {name} failed ,message : {message}  ")
            result = {"message":f" {message} ","timestamp" : timestamp,'status_code': 300}
            return jsonify(result)
    except Exception as e1:
        print(e1)
        return jsonify({'message': f'delete point failed,{e1}', 'status_code': 300})



@app.route('/delete_doc', methods=['POST'])
def delete_doc():
    try:
        # https://www.volcengine.com/docs/84313/1269161
        logger.info(f"===== delete_doc 用于从知识库删除文档 ====")
        path = '/api/knowledge/doc/delete'
        data = request.get_json()  # 从POST请求中获取数据
        print('data:',data)
        name = data['name']
        doc_id = data['doc_id']
        request_params ={
                        "collection_name": name,
                        "project": "",
                        "doc_id": doc_id }
        info_req = prepare_request(method = method, path = path, ak = ak, sk = sk,
                           data = request_params)
        res = requests.request(method=info_req.method,
                url = "https://{}{}".format(DOMAIN, info_req.path),
                headers = info_req.headers,
                data = info_req.body)
        ans = res.json()
        code =ans['code']
        if code == 0:
            logger.info(f" delete {doc_id} from collection {name} success  ")
            result = {"message":f" delete {doc_id} from collection {name} success ","timestamp" : timestamp ,'status_code': 200}
            return jsonify(result)
        else:
            message = ans['message']
            logger.info(f" delete {doc_id} from collection {name} failed ,message : {message}  ")
            result = {"message":f" {message} ","timestamp" : timestamp,'status_code': 300}
            return jsonify(result)
    except Exception as e1:
        print(e1)
        return jsonify({'message': f'delete_doc failed,{e1}', 'status_code': 300})


@app.route('/point_update', methods=['POST'])
def point_update():
    try:
        logger.info("=== point_update 更新知识库下的切片内容 ===")
        path ="/api/knowledge/point/update"
        data = request.get_json()  # 从POST请求中获取数据
        print('data: ',data)
        name = data['name']
        collection_type = data['collection_type']
        point_id = data['point_id']
        if collection_type == 0:
            #结构化数据集
            fields =data['fields']
            request_params ={
                "collection_name": name,
                "project": "",
                "point_id":point_id,
                "fields":fields
                          }
        else:
            content  = data['content']
            if 'question' not in data:
                request_params ={
                            "collection_name": name,
                            "project": "",
                            "point_id":point_id,
                            "content": content,
                            } 
            else:
                question =data['question']
                request_params ={
                            "collection_name": name,
                            "project": "",
                            "point_id":point_id,
                            "question":question,
                            "content": content,
                            }
        info_req = prepare_request(method = method, path = path, ak = ak, sk = sk,
                           data = request_params)
        res = requests.request(method=info_req.method,
                url = "https://{}{}".format(DOMAIN, info_req.path),
                headers = info_req.headers,
                data = info_req.body)
        ans = res.json()
        code =ans['code']
        if code == 0:
            logger.info(f"point update from collection {name} success  ")
            result = {"message":f"update  {point_id} from collection {name} success ","timestamp" : timestamp ,'status_code': 200}
            return jsonify(result)
        else:
            message = ans['message']
            logger.info(f" update  {point_id} from collection {name} failed ,message : {message}  ")
            result = {"message":f" {message} ","timestamp" : timestamp,'status_code': 300}
            return jsonify(result)
    except Exception as e1:
        print(e1)
        return jsonify({'message': f'update  {point_id} failed, {e1}', 'status_code': 300})






@app.route('/point_add', methods=['POST'])
def point_add():
    try:
        logger.info("=== point_add 新增一个知识库下某个文档的一个切片===")
        data = request.get_json()  # 从POST请求中获取数据
        print('data: ',data)
        name = data['name']
        collection_type =data['collection_type']
        doc_id = data['doc_id'] #  #doc_id 表示新增切片所属的文档
        chunk_type = data['chunk_type']
        path = '/api/knowledge/point/add'
        if collection_type == 0 and chunk_type=="structured":
            fields = data['fields']
            #print("fields:" ,fields)
            request_params ={
                "collection_name": name,
                "project": "",
                "doc_id": doc_id,
                "chunk_type":chunk_type, # 要添加的切片类型
                "fields": fields }
        elif collection_type == 1 and chunk_type=="faq":
            content  = data['content']
            question = data['question']
            #非结构化数据
            request_params ={
                "collection_name": name,
                "project": "",
                "doc_id": doc_id,
                "chunk_type":chunk_type, # 要添加的切片类型
                "question":question,
                "content": content }
        elif collection_type == 1 and chunk_type=="text":
            content  = data['content']
            request_params ={
                "collection_name": name,
                "project": "",
                "doc_id": doc_id,
                "chunk_type":chunk_type, # 要添加的切片类型
                "content": content }
        info_req = prepare_request(method = method, path = path, ak = ak, sk = sk,
                           data = request_params)
        res = requests.request(method=info_req.method,
                url = "https://{}{}".format(DOMAIN, info_req.path),
                headers = info_req.headers,
                data = info_req.body)
        ans = res.json()
        code =ans['code']
        if code == 0:
            logger.info(f"point add from collection {name} success  ")
            result = {"message":f"point add  {doc_id} from collection {name} success ","timestamp" : timestamp ,'status_code': 200}
            return jsonify(result)
        else:
            message = ans['message']
            logger.info(f"point add {doc_id} from collection {name} failed ,message : {message}  ")
            result = {"message":f" {message} ","timestamp" : timestamp,'status_code': 300}
            return jsonify(result)
    except Exception as e1:
        print(e1)
        return jsonify({'message': f'point add failed, {e1}', 'status_code': 300})




@app.route('/update_meta', methods=['POST'])
def update_meta():
    try:
        logger.info("=== update_meta 用于更新文档信息 ===")
        data = request.get_json()  # 从POST请求中获取数据
        print('data: ',data)
        name = data['name']
        doc_id = data['doc_id']
        meta =  data['meta']
        path = '/api/knowledge/doc/update_meta'
        request_params = {
                "collection_name": name,
                "project": "",
                "doc_id": doc_id,
                "meta": meta }
        info_req = prepare_request(method = method, path = path, ak = ak, sk = sk,
                           data = request_params)
        res = requests.request(method=info_req.method,
                url = "https://{}{}".format(DOMAIN, info_req.path),
                headers = info_req.headers,
                data = info_req.body)
        ans = res.json()
        code =ans['code']
        if code == 0:
            logger.info(f"update meta {doc_id} from collection {name} success  ")
            result = {"message":f"update meta {doc_id} from collection {name} success ","timestamp" : timestamp ,'status_code': 200}
            return jsonify(result)
        else:
            message = ans['message']
            logger.info(f"update meta {doc_id} from collection {name} failed ,message : {message}  ")
            result = {"message":f" {message} ","timestamp" : timestamp,'status_code': 300}
            return jsonify(result)
    except Exception as e1:
        print(e1)
        return jsonify({'message': f'update meta failed, {e1}', 'status_code': 300})

@app.route('/search_collection', methods=['POST'])
def search_collection():
    try:
        logger.info(f"===search_collection用于对知识库进行检索，支持文本检索====")
        path = '/api/knowledge/collection/search'
        # 修改查询字段为 '问题'
        data = request.get_json()  # 从POST请求中获取数据
        name = data['name']
        query =data['query']
        request_params = {
            "name": name,
            "project": "",
            "query": query,
            "retrieve_count": 5,
            "limit": 3,
            "query_param": {
                "doc_filter":   {
                    "op": "must",
                      # 修改为 '问题'
                    "conds": []  # 你要过滤的具体问题
                                },
                            },
            "rerank_switch": True,
            "dense_weight": 0.5
                        }
        info_req = prepare_request(method=method, path=path, ak=ak,
                                   sk=sk, data=request_params)
        res = requests.request(method=info_req.method,
                       url="https://{}{}".format(DOMAIN, info_req.path),
                       headers=info_req.headers,data=info_req.body)
        print(res.json())
        ans = res.json()

        return jsonify({"result":ans,'status_code': 200})
    except Exception as e1:
        print(e1)
        return jsonify({'message': f'search collection failed, {e1}', 'status_code': 300})





@app.route('/search_generate', methods=['POST'])
def search_generate():
    try:
        logger.info(f"===== search_and_generate 用于对知识库进行检索，并将检索到的文本片和用户问题组装到prompt当>中  =====")
        path = '/api/knowledge/collection/search'
        data = request.get_json()  # 从POST请求中获取数据
        name = data['name']
        query =data['query']
        request_params = {
            "name": name,
            "project": "",
            "query": query, #职位的具体工作内容是什么
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
            "prompt": "你是一位在线客服，你的首要任务是通过巧妙的话术回复用户的问题，你需要根据「参考资料」来回答接下来的「用户问题,这些信息在 <context></context> XML tags 之内.\n\n<context>\n{{.retrieved_chunks}}\n</context>\n\n回答用户的问题,用户的问题在<query></query> XML tags 之内\n回答问题时,你需要根据参考资料给出准确,简洁的回答\n\n<query>\n{{.user_query}}\n</query>",
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
        result =[ ]
        ans = res.json()
        for i in ans['data']['result_list']:
            result.append(i)
        print('search_and_generate:' ,result)
        json_string = result[0]['doc_info']['doc_meta']
        parsed_json = json.loads(json_string)
        return jsonify({"result":result,'status_code': 200})

    except Exception as e:
        print(e)
        return jsonify({'message': f'search_and_generate failed, {e}', 'status_code': 300})




@app.route('/search_knowledge', methods=['POST'])
def search_knowledge():
    try:
        logger.info(f"===== search_knowledge 用于对知识库进行检索和前后处理  =====")
        data = request.get_json()  # 从POST请求中获取数据
        name = data['name']
        query =data['query']
        pre_processing = {
             "need_instruction": True,
             "rewrite": True,
             "messages": [
                 {
                     "role": "system",
                     "content": ""
                 },
                 {
                     "role": "user",
                     "content": "" # messages 最后一个元素的content和query保持一致
                 }
                         ],
            "return_token_usage": True
                 }
        post_processing = {
             "rerank_switch": True,
             "rerank_model": "Doubao-pro-4k-rerank",
             "rerank_only_chunk": False,
             'chunk_diffusion_count': 2,
             "retrieve_count": 5,
            #  "endpoint_id": "ep-20240725211310-b28mr",
             "chunk_group": True,
             "get_attachment_link": True
         }
        res = viking_knowledgebase_service.search_knowledge(
                   collection_name = name,query = query,
                   pre_processing = pre_processing, limit = 5, dense_weight = 0.5,
                   post_processing = post_processing, project = "default")

        rewrite_query = res['rewrite_query']
        content_list = []
        for i in res['result_list']:
            #print(i)
            content = i['content']
            score =i['score']
            chunk_title = i['chunk_title']
            if ('rerank_score' in i)  and ('rerank_position' in i) and ('recall_position' in i):
                rerank_score = i['rerank_score']
                rerank_position = i['rerank_position']
                recall_position = i['recall_position']
                content_list.append({"content": content, "chunk_title":chunk_title,"score":score,
                              "rerank_score":rerank_score,"recall_position":recall_position,
                              "rerank_position":rerank_position})
            else:
                content_list.append({"content": content , "chunk_title":chunk_title,"score":score})

        result ={"query":query,"rewrite_query":rewrite_query,"content_list":content_list}
        print("===result===", result)
        logger.info(f"result: {result} ")
        return jsonify({"result":result,'status_code': 200})
    except Exception as e:
        print(e)
        logger.info(f"query: {query},error:{e}")
        return jsonify({'message': f'search_knowledge failed, {e}', 'status_code': 300})



@app.route('/chat_llm', methods=['POST'])
def chat_llm():
    try:
        logger.info(f"===== chat_llm向大模型发起一次对话请求  =====")
        model = "Doubao-pro-32k"
        data = request.get_json()  # 从POST请求中获取数据
        print('data:',data)
        logger.info(f"chat_llm input :{data}")
        query =data['query']
        m_messages = [{
                "role": "system",
                "content": """ 你是智能助手，你擅长以老师的身份，并用亲切幽默的风格回答用户的问题"""
                        },
                    {
                "role": "user",
                "content": query # 用户提问
                     }
                     ]
        res = viking_knowledgebase_service.chat_completion(model=model, messages=m_messages, max_tokens=4096,
                                                        temperature=0.1)
        print(res['generated_answer'])
        answer =  res['generated_answer']
        result ={"query":query,"answer":answer}
        logger.info(f"result: {result} ")
        return jsonify({"result":result,'status_code': 200})

    except Exception as e:
        print(e)
        logger.info(f"query: {query},error:{e}")

        




@app.route('/search_chat_llm', methods=['POST'])
def search_chat_llm():
    try:
        logger.info(f"===== search_chat_llm  =====")
        path = "/api/knowledge/collection/search_knowledge"
        data = request.get_json()  # 从POST请求中获取数据
        #print('data:',data)
        start =time.time()
        logger.info(f"search_chat_llm input :{data}")
        name = data['name']
        query =data['query']
        request_params = {
                 "project": "default",
                "name": name,
                "query": query,
                "limit": 3,
                "pre_processing":  {
                "need_instruction": True,
                "rewrite": False,
                "return_token_usage": True,
                "messages": [
                            {
                                "role": "system",
                                "content": ""
                             },
                            {
                                "role": "user",
                                "content": ""
                            }
                            ]
                                    },
                "dense_weight": 0.5,
                "post_processing": 
                        {
                            "get_attachment_link": True,
                            "chunk_group": True,
                            "rerank_only_chunk": False,
                            "rerank_switch": True,
                            "chunk_diffusion_count": 0
                        }
                }
    
        info_req = prepare_request(method=method, 
                    path="/api/knowledge/collection/search_knowledge" ,
                    ak=ak, sk=sk, data=request_params)
        rsp = requests.request(
                                method=info_req.method,
                                url="http://{}{}".format(DOMAIN, info_req.path),
                                headers=info_req.headers,
                                data=info_req.body
                                )
        #1. 执行search_knowledge 得到相关知识片段
        rsp_txt = rsp.text 
        #print('rsp_txt:' ,rsp_txt)
        # 2.generate_prompt  生成prompt 
        prompt = generate_prompt(rsp_txt) 
        # 3.拼接message对话, 问题对应role为user，系统对应role为system
        #   答案对应role为assistant, 内容对应content
        messages =[{"role": "system",
                      "content": prompt},
                    {"role": "user", "content": query}]
        # 4.调用chat_completion
        #cost_time = end -start
        #print("cost_time:" ,cost_time)
        answer, usage  =  chat_completion(messages,stream=False, return_token_usage=True,
                    temperature=0.7, max_tokens=4096)
        cost_time = time.time() -start
        logger.info(f"query: {query},answer:{answer} ,cost_time:{cost_time}")
        return jsonify({"result":answer,'usage':usage ,'status_code': 200})

    except Exception as e:
        print(e)
        logger.info(f"query: {query},error:{e}")
        return jsonify({'message': f'search_knowledge_and_chat_completion failed, {e}',
                        'status_code': 300})


@app.route('/chat', methods=['POST'])
def chat():
    try:
        logger.info(f"===== chat =====")
        path = "/api/knowledge/collection/search_knowledge"
        data = request.get_json()  # 从POST请求中获取数据
        print('data:',data)
        logger.info(f"stream chat  :{data}")
        name = data['name']
        query =data['query']
        start =time.time()
        request_params = {
                 "project": "default",
                "name": name,
                "query": query,
                "limit": 5,
                "pre_processing":  {
                "need_instruction": True,
                "rewrite": False,
                "return_token_usage": True,
                "messages": [
                            {
                                "role": "system",
                                "content": ""
                             },
                            {
                                "role": "user",
                                "content": ""
                            }
                            ]
                                    },
                "dense_weight": 0.5,
                "post_processing":
                        {
                            "get_attachment_link": True,
                            "chunk_group": True,
                            "rerank_only_chunk": False,
                            "rerank_switch": True,
                             "chunk_diffusion_count": 0
                        }
                }

        info_req = prepare_request(method=method,
                    path="/api/knowledge/collection/search_knowledge" ,
                    ak=ak, sk=sk, data=request_params)
        rsp = requests.request(
                                method=info_req.method,
                                url="http://{}{}".format(DOMAIN, info_req.path),
                                headers=info_req.headers,
                                data=info_req.body
                                )
        #1. 执行search_knowledge 得到相关知识片段
        rsp_txt = rsp.text
        #print('相关知识:' ,rsp_txt)
        ans = json.loads(rsp_txt)
        prompt = generate_prompt(rsp_txt)
        print("prompt:",prompt)
        messages =[{"role": "system",
                      "content": prompt},
                    {"role": "user", "content": query}]
        from volcenginesdkarkruntime import Ark

        client = Ark(
                 base_url="https://ark.cn-beijing.volces.com/api/v3", api_key="f62bafd2-1269-4169-b072-7994b36541a7")
        stream = client.chat.completions.create(
                model="doubao-1-5-pro-32k-250115", messages = messages ,stream=True)

        def generate_Data():
            try:
                for chunk in stream:
                    if not chunk.choices:
                        continue
                    content = chunk.choices[0].delta.content
                    yield f"event:message\ndata:{content}\n\n"
                    delay =random.uniform(0.001,0.01)
                    time.sleep(delay)
            except Exception as e:
                 yield f"event: error\ndata: An error occurred: {str(e)}\n\n"
            yield "data: END_OF_STREAM\n\n"
        end_time = time.time()  # 记录请求结束时间
        logger.info(f"cost time: {end_time - start}")
        return Response(generate_Data(), mimetype='text/event-stream')
    
    except Exception as e:
        print(e)
        logger.info(f"query: {query},error:{e}")
        return jsonify({'message': f'chat_stream failed, {e}',
                        'status_code': 300})


    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)



