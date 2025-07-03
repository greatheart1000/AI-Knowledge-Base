import json
import os


from volcengine.viking_knowledgebase import VikingKnowledgeBaseService
viking_knowledgebase_service = VikingKnowledgeBaseService(host="api-knowledgebase.mlp.cn-beijing.volces.com", scheme="https", connection_timeout=30, socket_timeout=30)
viking_knowledgebase_service.set_ak("AKLTMWRhNmY2ZTZlZTNlNDYxMTk5MzBhOGNlNzczZDU5MGY")
viking_knowledgebase_service.set_sk("T0dSa1pETTVPR1UyWldVNU5EUXlZVGs1TXpnNU5XVTFOVFJsTnpBek5EWQ==")


datas =[{
        "query": "机器学习",
        "content": "机器学习是一种通过分析数据来自动推断模式并做出预测的技术。",

    }, {
        "query": "机器学习",
        "content": "深度学习是机器学习的一个子领域，它通过构建类似于人脑神经网络的多层结构来学习复杂数据。",

    }, {
        "query": "机器学习",
        "content": "监督学习是一种机器学习的方式，数据集由输入和对应的输出组成，模型通过学习这些映射来做出预测。",

    }, {
        "query": "机器学习",
        "content": "强化学习是一种机器学习方法，模型通过不断尝试和错误来学习最佳策略。",

    }]
res = viking_knowledgebase_service.rerank(datas=datas, rerank_model="m3-v2-rerank")
print(res)

