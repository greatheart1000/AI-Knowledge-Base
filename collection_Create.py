#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/18 16:01
# @Author  : caijian
# @File    : collection_Create.py
# @Software: PyCharm
from utils import ak,sk
from volcengine.viking_knowledgebase import VikingKnowledgeBaseService, Collection, Doc, Point
from volcengine.viking_knowledgebase.common import Field, FieldType, IndexType, EmbddingModelType

viking_knowledgebase_service = VikingKnowledgeBaseService(host="api-knowledgebase.mlp.cn-beijing.volces.com")
viking_knowledgebase_service.set_ak(ak)
viking_knowledgebase_service.set_sk(sk)

collection_name = "your_collection_name"
description = "111"

# 默认参数构建知识库
my_collection = viking_knowledgebase_service.create_collection(collection_name)

# 自定义index配置、preprocess文档配置构建知识库
index = {
   "index_type": IndexType.HNSW_HYBRID,
   "index_config": {
        "fields": [
                {"field_name": "行业", "field_type": "list<string>"},
                {"field_name": "是否公开", "field_type": "bool"},
                {'field_name': '重要性', 'field_type': 'list<string>'}],
        "cpu_quota": 1,
        "quant": "int8",
        "embedding_dimension": 2048,
        "embedding_model":EmbddingModelType.EmbeddingModelBgeLargeZhAndM3
  }
}
preprocessing = {
    "chunking_strategy":"custom_balance",
                "chunk_length":2000,
                "merge_small_chunks":True,
                "multi_modal":["image_ocr"]

}
my_collection = viking_knowledgebase_service.create_collection(
    collection_name=collection_name,
    description=description,
    index=index,
    preprocessing=preprocessing,
    data_type="unstructured_data")

# 获取collection详细信息
my_collection = viking_knowledgebase_service.get_collection(collection_name=collection_name)

# # 由tos路径上传doc
# tos_path = ""
# my_collection.add_doc(add_type="tos", tos_path=tos_path)
#
# # 由url上传doc
# url = "your url"
# my_collection.add_doc(add_type="url", doc_id="your_doc_id", doc_name="your_doc_name", doc_type="", url=url)
#
# # 查询
# query = ""
# points = viking_knowledgebase_service.search_collection(collection_name=collection_name, query=query)
#
# for point in points:
#     print(point.content)
#     print(point.score)