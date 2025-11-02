#coding:utf-8
#get_doc用于查看知识库下的某个文档的信息。
from volcengine.viking_knowledgebase import VikingKnowledgeBaseService
from utils import ak,sk
viking_knowledgebase_service = VikingKnowledgeBaseService(
    host="api-knowledgebase.mlp.cn-beijing.volces.com",
    scheme="https", connection_timeout=30, socket_timeout=30)
viking_knowledgebase_service.set_ak(ak)
viking_knowledgebase_service.set_sk(sk)
my_collection = viking_knowledgebase_service.get_collection("ppt111")
doc = my_collection.get_doc("doc_001")
print(doc.collection_name)
# 文档下知识点数量
print(doc.point_num)
#文档名字
print(doc.doc_name)
print(doc.url)
print(doc.added_by)
print(doc.source)
print(doc.fields)

