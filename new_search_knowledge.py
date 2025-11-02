#coding:utf-8
#get_doc用于查看知识库下的某个文档的信息。
ak = '#####################################################'
sk = '#####################################################'
from volcengine.viking_knowledgebase import VikingKnowledgeBaseService
viking_knowledgebase_service = VikingKnowledgeBaseService(
    host="api-knowledgebase.mlp.cn-beijing.volces.com",
    scheme="https", connection_timeout=30, socket_timeout=30)
viking_knowledgebase_service.set_ak(ak)
viking_knowledgebase_service.set_sk(sk)
collection_name = "unstructure_Data"
query ="个人评价"
pre_processing = {
             "need_instruction": True,
             "rewrite": False,
             "messages": [
                 {
                     "role": "system",
                     "content": "",
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
            #  'chunk_diffusion_count': 2,
             "retrieve_count": 5,
            #  "endpoint_id": "ep-20240725211310-b28mr",
             "chunk_group": True,
             "get_attachment_link": True
         }
doc_filter = {
    "op": "must",
    "field":  'category',
    "conds": ["招聘行业"]
}
query_param = {
    "doc_filter": doc_filter
}
res = viking_knowledgebase_service.search_knowledge(
collection_name=collection_name,query=query,
query_param=None ,pre_processing=pre_processing,
limit=5, dense_weight=0.5,post_processing=post_processing, project="default")

print(res)
