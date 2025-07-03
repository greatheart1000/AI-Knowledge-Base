{"prompt": "使用以下的信息作为你学习到的知识，这些信息在 <context></context> XML"
           " tags 之内.\n\n<context>\n{{.retrieved_chunks}}\n</context>\n\n"
           "回答用户的问题，用户的问题在<query></query> XML tags 之内\n回答问题时，"
           "如果你不知道，请直接说明你不知道。\n\n<query>\n{{.user_query}}\n</query>",
 }
{"prompt":"""你是一位在线客服，你的首要任务是通过巧妙的话术回复用户的问题，你需要根据「参考资料」来回答接下来的「用户问题」，这些信息在 <context></context> XML tags 之内，你需要根据参考资料给出准确，简洁的回答。


你的回答要满足以下要求：
    1. 回答内容必须在参考资料范围内，尽可能简洁地回答问题，不能做任何参考资料以外的扩展解释。
    2. 回答中需要根据客户问题和参考资料保持与客户的友好沟通。
    3. 如果参考资料不能帮助你回答用户问题，告知客户无法回答该问题，并引导客户提供更加详细的信息。
    4. 为了保密需要，委婉地拒绝回答有关参考资料的文档名称或文档作者等问题。

# 任务执行
现在请你根据提供的参考资料，遵循限制来回答用户的问题，你的回答需要准确和完整。


# 参考资料
<context>
  <Documents>

</context>
"""}


#
# "prompt": "使用以下的信息作为你学习到的知识，这些信息在 <context></context> XML tags 之内.\n\n<context>\n{{.retrieved_chunks}}\n</context>\n\n回答用户的问题，用户的问题在<query></query> XML tags 之内\n回答问题时，如果你不知道，请直接说明你不知道。\n\n<query>\n{{.user_query}}\n</query> "
#
# """<context></context>  是 search之后的结果
# 用户的问题在<query></query> XML tags 之内 是用户输入的问题
#
# """

extracted_entities_prompt ="请从以下文本中提取所有实体（人名、地点、组织等）：\n\n[text]\n\n返回的格式为：\n[['实体1', '类型'], ['实体2', '类型'], ...]"

summarized_entities_prompt ="请对以下实体进行总结，合并相似的实体，并保持信息的完整性：\n\n[entities]\n\n返回的格式为：\n[['总结实体1', '类型'], ['总结实体2', '类型'], ...]"

create_base_entity_graph_prompt = "根据以下实体，构建一个基础实体图，描述实体之间的关系：\n\n[entities]\n\n返回的格式为：\n[['实体1', '关系', '实体2'], ['实体3','关系', '实体4' ], ...]"

create_final_entities_prompt = "请对以下实体进行去重和清洗，返回最终的实体集合：\n\n[entities]\n\n返回的格式为：\n[['最终实体1', '类型'], ['最终实体2', '类型'], ...]"

create_final_nodes_prompt ="根据以下实体生成图节点的描述：\n\n[entities]\n\n返回的格式为：\n[['节点ID', '实体名'], ['节点ID', '实体名'], ...]"


generate_knowledge_graph_prompt= """
    根据以下信息生成知识图谱：

    1. 实体之间的关系：
    [relationships]

    2. 总结实体及其类型：
    [summarized_entities]

    3. 图节点信息：
    [final_nodes]

    请将这些信息结合起来，描述如何构建知识图谱，包括节点、边及其特性，并给出图的整体结构示例。返回的格式应包括节点和边的详细信息，例如：
    {
        "nodes": [["节点ID", "实体名", "类型"], ...],
        "edges": [["实体1节点ID", "实体2节点ID", "关系类型"], ...]
    }
    """
