from typing import Dict, TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

# 请设置你的 API 密钥
# import os
# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

# 定义状态
class AgentState(TypedDict):
    """
    智能体状态。用于在节点间传递信息。
    """
    user_query: str
    retrieved_docs: str
    generated_response: str
    reflection_result: str
    human_in_the_loop: bool = False

# 定义各个节点（功能模块）

# 1. 规划节点
def plan_node(state: AgentState) -> Dict:
    """
    根据用户问题判断是否需要检索。
    """
    print("---执行：规划---")
    user_query = state["user_query"]
    # 简单的关键词判断，实际中会使用LLM来做复杂判断
    if "向量数据库" in user_query or "RAG" in user_query:
        print("---结论：需要检索外部知识---")
        return {"next_node": "rag_node"}
    else:
        print("---结论：可以直接生成答案---")
        return {"next_node": "generate_node"}

# 2. RAG 节点
def rag_node(state: AgentState) -> Dict:
    """
    模拟从向量数据库检索文档。
    """
    print("---执行：检索---")
    user_query = state["user_query"]
    # 这是一个简化版的检索，实际中会调用Milvus, Chroma等
    mock_db = {
        "什么是向量数据库": "向量数据库是用来存储和检索向量化数据的数据库，尤其适用于语义搜索和相似性匹配。它在大模型RAG（检索增强生成）应用中扮演核心角色。",
        "LangGraph是什么": "LangGraph是一个用于构建复杂LLM工作流的库，它以图的形式组织不同的节点和流程。"
    }
    retrieved_docs = mock_db.get(user_query, "未找到相关文档。")
    print(f"---检索结果：{retrieved_docs[:20]}...---")
    return {"retrieved_docs": retrieved_docs}

# 3. 生成节点
def generate_node(state: AgentState) -> Dict:
    """
    结合检索结果生成最终答案。
    """
    print("---执行：生成答案---")
    model = ChatOpenAI(temperature=0)
    prompt = f"请根据以下信息回答问题：\n问题：{state['user_query']}\n相关信息：{state['retrieved_docs']}\n答案："
    # 这是一个简化版的生成，实际会调用大模型API
    response = model.invoke(prompt)
    print(f"---生成的答案：{response.content[:20]}...---")
    return {"generated_response": response.content}

# 4. 反思节点
def reflect_node(state: AgentState) -> Dict:
    """
    反思生成的答案是否合格。
    """
    print("---执行：反思---")
    generated_response = state["generated_response"]
    # 模拟反思逻辑：检查答案中是否提到了'向量数据库'
    if "向量数据库" in generated_response:
        print("---反思结果：答案符合要求，可以结束---")
        return {"reflection_result": "pass"}
    else:
        print("---反思结果：答案不完整，需要人工介入---")
        return {"reflection_result": "fail"}

# 5. 人类介入节点
def human_in_the_loop_node(state: AgentState) -> Dict:
    """
    模拟人工介入。
    """
    print("---执行：人工介入，等待处理---")
    # 这里可以暂停流程，将任务发给人工队列
    # 也可以直接返回一个标志，让流程在下一步结束
    return {"human_in_the_loop": True}

# 构建 LangGraph 图
workflow = StateGraph(AgentState)

# 添加节点
workflow.add_node("plan_node", plan_node)
workflow.add_node("rag_node", rag_node)
workflow.add_node("generate_node", generate_node)
workflow.add_node("reflect_node", reflect_node)
workflow.add_node("human_in_the_loop_node", human_in_the_loop_node)

# 设置入口
workflow.set_entry_point("plan_node")

# 定义边
# 条件边：根据 plan_node 的结果决定下一步
workflow.add_conditional_edges(
    "plan_node",
    lambda state: state["next_node"],
    {
        "rag_node": "rag_node",
        "generate_node": "generate_node",
    }
)

# 常规边：rag_node 执行完后，进入 generate_node
workflow.add_edge("rag_node", "generate_node")

# 常规边：generate_node 执行完后，进入 reflect_node
workflow.add_edge("generate_node", "reflect_node")

# 条件边：根据 reflect_node 的结果决定下一步
workflow.add_conditional_edges(
    "reflect_node",
    lambda state: state["reflection_result"],
    {
        "pass": END,  # 如果反思通过，流程结束
        "fail": "human_in_the_loop_node", # 否则，需要人工介入
    }
)

# 常规边：人工介入节点，流程结束
workflow.add_edge("human_in_the_loop_node", END)

# 编译图，得到可执行的 app
app = workflow.compile()

# 运行智能体
print("\n---测试用例 1: 复杂问题 (需要 RAG)---")
app.invoke({"user_query": "什么是向量数据库"})

print("\n---测试用例 2: 简单问题 (直接生成)---")
app.invoke({"user_query": "LangGraph是什么"})
