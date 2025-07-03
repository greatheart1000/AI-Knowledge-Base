#coding:utf-8
"""生成了文档每个知识切片的知识图谱的过程"""

import json
import requests
import logging
from utils import prepare_request
from utils import ak, sk ,method,DOMAIN # 假设这是您的API密钥模块
from RAG_prompts import extracted_entities_prompt ,summarized_entities_prompt,\
    create_base_entity_graph_prompt,create_final_entities_prompt,\
    create_final_nodes_prompt,generate_knowledge_graph_prompt,summarize_and_extract_keywords_prompt

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='knowledge_graph.log')


class KnowledgeGraphGenerator:
    def __init__(self, api_url, api_key, model_name,collection_name):
        self.url = api_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        self.model_name = model_name
        self.collection_name = collection_name
        self.summarize_and_extract_keywords_prompt = summarize_and_extract_keywords_prompt
        self.extracted_entities_prompt = extracted_entities_prompt
        self.summarized_entities_prompt = summarized_entities_prompt
        self.create_base_entity_graph_prompt = create_base_entity_graph_prompt
        self.create_final_entities_prompt = create_final_entities_prompt
        self.create_final_nodes_prompt = create_final_nodes_prompt
        self.generate_knowledge_graph_prompt = generate_knowledge_graph_prompt

    def call_large_language_model(self, prompt):
        data = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
        result = response.json()['choices'][0]['message']['content']
        print(result)
        return result


    def extract_points_from_knowledge_base(self):
        path = '/api/knowledge/point/list'
        request_params = {
            "collection_name": self.collection_name,
            "project": ""
        }
        info_req = prepare_request(method=method, path=path, ak=ak, sk=sk, data=request_params)
        res = requests.request(method=info_req.method,
                               url="https://{}{}".format(DOMAIN, info_req.path),
                               headers=info_req.headers,
                               data=info_req.body)
        ans = res.json()
        points = []
        for i in ans['data']['point_list']:
            point_id = i['point_id']
            content = i['content']
            points.append((point_id, content))
            logging.info('point_id: %s, content: %s', point_id, content)
        return points

    def process_knowledge_graph(self):
        points = self.extract_points_from_knowledge_base()
        print('points',points)
        result =[]
        for point_id, content in points:
            logging.info('Processing point_id: %s', point_id)

            # 逐步执行知识图谱生成
            extracted_summary_keywords = self.summarize_and_extract_keywords(content)
            entities = self.extracted_entities(content)

            summarized_entities = self.summarized_entities(entities)
            relationships_entity = self.create_base_entity_graph(summarized_entities)
            final_entities = self.create_final_entities(relationships_entity)
            final_nodes = self.create_final_nodes(final_entities)
            knowledge_graph = self.generate_knowledge_graph(relationships_entity, summarized_entities, final_nodes)

            # 记录生成的知识图谱
            logging.info('知识图谱生成成功 for point_id: %s', point_id)
            logging.info('知识图谱: %s', knowledge_graph)


    def summarize_and_extract_keywords(self, text):
        prompt = self.summarize_and_extract_keywords_prompt.replace('[text]', text)
        result = self.call_large_language_model(prompt)
        logging.info('[步骤0] 提取文本中的摘要和关键词: %s', result)
        return result

    def extracted_entities(self, text):
        prompt = self.extracted_entities_prompt.replace('[text]', text)
        result = self.call_large_language_model(prompt)
        logging.info('[步骤1] 文本中提取所有实体: %s', result)
        return result

    def summarized_entities(self, entities):
        prompt = self.summarized_entities_prompt.replace('[entities]', entities)
        result = self.call_large_language_model(prompt)
        logging.info('[步骤2] 对实体进行总结: %s', result)
        return result

    def create_base_entity_graph(self, entities):
        prompt = self.create_base_entity_graph_prompt.replace('[entities]', entities)
        result = self.call_large_language_model(prompt)
        logging.info('[步骤3] 根据实体构建基础实体图: %s', result)
        return result

    def create_final_entities(self, entities):
        prompt = self.create_final_entities_prompt.replace('[entities]', entities)
        result = self.call_large_language_model(prompt)
        logging.info('[步骤4] 对实体进行去重和清洗: %s', result)
        return result

    def create_final_nodes(self, entities):
        prompt = self.create_final_nodes_prompt.replace('[entities]', entities)
        result = self.call_large_language_model(prompt)
        logging.info('[步骤5] 根据实体生成图节点描述: %s', result)
        return result

    def generate_knowledge_graph(self, relationships, summarized_entities, final_nodes):
        prompt = self.generate_knowledge_graph_prompt.replace('[relationships]', relationships).replace('[summarized_entities]', summarized_entities).replace(
            '[final_nodes]', final_nodes)
        result = self.call_large_language_model(prompt)
        logging.info('[步骤6] 根据实体之间的关系生成知识图谱: %s', result)
        return result


# 示例使用
if __name__ == "__main__":
    api_url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    api_key = "f62bafd2-1269-4169-b072-7994b36541a7"  # 替换为您的实际 API 密钥
    model_name = "ep-20241105171007-x2j89"  # 替换为您的实际模型名称
    collection_name='"unstructure_Data"'
    generator = KnowledgeGraphGenerator(api_url, api_key, model_name,collection_name)
    generator.process_knowledge_graph()