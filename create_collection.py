# from volcengine.viking_knowledgebase import VikingKnowledgeBaseService
# from utils import ak,sk
# viking_knowledgebase_service = VikingKnowledgeBaseService(
#     host="api-knowledgebase.mlp.cn-beijing.volces.com",
#     scheme="https", connection_timeout=30, socket_timeout=30)
# viking_knowledgebase_service.set_ak(ak)
# viking_knowledgebase_service.set_sk(sk)
# collection_name = "example"
# description = "This is an example"
# # 自定义index配置、preprocess文档配置构建知识库
# index = {
#     "index_type": IndexType.HNSW_HYBRID,
#     "index_config": {
#         "fields": [{
#             "field_name": "chunk_len",
#             "field_type": FieldType.Int64,
#             "default_val": 32
#         }],
#         "cpu_quota": 1,
#         "embedding_model": EmbddingModelType.EmbeddingModelBgeLargeZhAndM3
#     }
# }
# preprocessing = {
#     "chunk_length": 200,
# }
# my_collection = viking_knowledgebase_service.create_collection(collection_name = collection_name,
#                                                                description = description, index = index, preprocessing = preprocessing)