import requests
import json
import logging
from RAG_prompts import extracted_entities_prompt ,summarized_entities_prompt,\
    create_base_entity_graph_prompt,create_final_entities_prompt,\
    create_final_nodes_prompt,generate_knowledge_graph_prompt,summarize_and_extract_keywords_prompt

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='knowledge_graph.log')


class KnowledgeGraphGenerator:
    def __init__(self, api_url, api_key, model_name):
        self.url = api_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        self.model_name = model_name
        self.summarize_and_extract_keywords_prompt = summarize_and_extract_keywords_prompt
        self.extracted_entities_prompt =extracted_entities_prompt
        self.summarized_entities_prompt =summarized_entities_prompt
        self.create_base_entity_graph_prompt =create_base_entity_graph_prompt
        self.create_final_entities_prompt =create_final_entities_prompt
        self.create_final_nodes_prompt =create_final_nodes_prompt
        self.generate_knowledge_graph_prompt =generate_knowledge_graph_prompt


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

    def summarize_and_extract_keywords(self, text):
        prompt =self.summarize_and_extract_keywords_prompt.replace('[text]', text)
        result = self.call_large_language_model(prompt)
        logging.info('[步骤0] 提取文本中的摘要和关键词: %s', result)
        return result

    def extracted_entities(self, text):
        prompt = self.extracted_entities_prompt.replace('[text]',                                                                                                     text)
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
        prompt = self.create_final_entities_prompt.replace('[entities]',entities)
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
    generator = KnowledgeGraphGenerator(api_url, api_key, model_name)
    text = """传统的办公自动化（OA）系统与现代协作式OA系统之间存在显著的区别，主要体现在以下几个方面：
    1. 功能范围：
    传统OA系统：主要关注于文档处理、电子邮件、日程安排等基本功能。这些系统通常是独立的应用程序，功能相对单一。
    协作式OA系统：集成了更多的功能模块，如即时通讯、项目管理、在线协作编辑、视频会议等，支持更广泛的办公需求。
    2. 用户体验：
    传统OA系统：界面设计和用户体验较为基础，操作流程可能较为复杂。
    协作式OA系统：注重用户体验，界面友好，操作简便，通常支持移动设备访问，提供更好的用户交互体验。"""

    # 逐步执行
    extracted_summary_keywords = generator.summarize_and_extract_keywords(text)

    entities = generator.extracted_entities(text)

    summarized_entities = generator.summarized_entities(entities)

    relationships_entity = generator.create_base_entity_graph(summarized_entities)

    final_entities = generator.create_final_entities(relationships_entity)

    final_nodes = generator.create_final_nodes(final_entities)

    knowledge_graph = generator.generate_knowledge_graph(relationships_entity, summarized_entities, final_nodes)