#coding:utf-8
import requests
import json
url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer f62bafd2-1269-4169-b072-7994b36541a7"  # 替换为您的实际 API 密钥
}

from prompts_mangement import extracted_entities_prompt ,summarized_entities_prompt,\
    create_base_entity_graph_prompt,create_final_entities_prompt,\
    create_final_nodes_prompt,generate_knowledge_graph_prompt

def create_base_extracted_entities(text):
    data = {
    "model": "ep-20241105171007-x2j89",  # 替换为您的实际模型名称
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": extracted_entities_prompt.replace('[text]',text)  }
    ]
}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    # 打印响应内容
    result =response.json()['choices'][0]['message']['content']
    print('[step1] 文本中提取所有实体（人名、地点、组织等）:',result)
    return result

def create_summarized_entities(text):
    data = {
    "model": "ep-20241105171007-x2j89",  # 替换为您的实际模型名称
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": summarized_entities_prompt.replace('[entities]',text)  }
    ]
}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    # 打印响应内容
    result =response.json()['choices'][0]['message']['content']
    print('[step2] 对实体进行总结，合并相似的实体，并保持信息的完整性:',result)
    return result

def create_base_entity_graph(text):
    data = {
        "model": "ep-20241105171007-x2j89",  # 替换为您的实际模型名称
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": create_base_entity_graph_prompt.replace('[entities]', text)}
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    # 打印响应内容
    result = response.json()['choices'][0]['message']['content']
    print('[step3] 根据实体构建一个基础实体图，描述实体之间的关系:',result)
    return result

def create_final_entities(text):
    data = {
        "model": "ep-20241105171007-x2j89",  # 替换为您的实际模型名称
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": create_final_entities_prompt.replace('[entities]', text)}
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    # 打印响应内容
    result = response.json()['choices'][0]['message']['content']
    print('[step4]对实体进行去重和清洗，返回最终的实体集合:',result)
    return result

def create_final_nodes(text):
    data = {
        "model": "ep-20241105171007-x2j89",  # 替换为您的实际模型名称
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": create_final_nodes_prompt.replace('[entities]', text)}
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    # 打印响应内容
    result = response.json()['choices'][0]['message']['content']
    print('[step5] 根据实体生成图节点的描述:',result)
    return result

def generate_knowledge_graph(relationships, summarized_entities, final_nodes):
    data = {
        "model": "ep-20241105171007-x2j89",  # 替换为您的实际模型名称
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": generate_knowledge_graph_prompt.replace('[relationships]', relationships).replace('[summarized_entities]', summarized_entities).replace('[final_nodes]', final_nodes)}
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    # 打印响应内容
    result = response.json()['choices'][0]['message']['content']
    print('[step6]  根据实体之间的关系、实体类型、图节点信息构建知识图谱:',result)
    return result



result = create_base_extracted_entities(text="""传统的办公自动化（OA）系统与现代协作式OA系统之间存在显著的区别，主要体现在以下几个方面：
1. 功能范围：
传统OA系统：主要关注于文档处理、电子邮件、日程安排等基本功能。这些系统通常是独立的应用程序，功能相对单一。
协作式OA系统：集成了更多的功能模块，如即时通讯、项目管理、在线协作编辑、视频会议等，支持更广泛的办公需求。
2. 用户体验：
传统OA系统：界面设计和用户体验较为基础，操作流程可能较为复杂。
协作式OA系统：注重用户体验，界面友好，操作简便，通常支持移动设备访问，提供更好的用户交互体验。
3. 协作能力：
传统OA系统：协作功能有限，主要依赖于电子邮件和文件共享，实时协作能力较弱。
协作式OA系统：强调团队协作，支持多人实时编辑、在线讨论、任务分配和进度跟踪，提升团队工作效率。
4. 数据存储与安全：
传统OA系统：数据通常存储在本地服务器，安全性依赖于企业内部的IT基础设施。
协作式OA系统：通常基于云计算，数据存储在云端，提供更高的安全性和数据备份能力，同时支持远程访问。
5. 智能化程度：
传统OA系统：智能化程度较低，主要依赖于用户手动操作。
协作式OA系统：集成了人工智能技术，能够自动化处理某些任务，如智能日程安排、自动提醒、数据分析等。
集成能力：
传统OA系统：与其他系统的集成能力有限，通常需要手动导入导出数据。""")

text= create_summarized_entities(result)

relationships_entity = create_base_entity_graph(text)

summarized_entities = create_final_entities(relationships_entity )

final_nodes= create_final_nodes(summarized_entities)

knowledge_graph =generate_knowledge_graph(relationships_entity, summarized_entities, final_nodes)
