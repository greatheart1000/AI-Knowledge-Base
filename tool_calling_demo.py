#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
使用 LangGraph 和 LangChain 实现工具调用示例。
该脚本展示了如何构建一个代理，使其能够根据用户输入自动调用外部工具。
"""

import os
from typing import TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field

# ----------------- 1. 定义工具 -----------------
# 我们使用 @tool 装饰器来创建可被模型调用的函数。

@tool
def image_generation_tool(description: str) -> str:
    """
    一个用于根据文本描述生成图片的工具。
    输入参数:
        - description (str): 描述你希望生成的图片内容。
    """
    print(f"\n--- 正在调用文生图工具 ---")
    print(f"输入描述: '{description}'")
    # 这里是一个模拟的图片生成过程，实际应用中会调用DALL-E, Stable Diffusion等API
    return f"图片已根据描述 '{description}' 生成。你可以点击这里查看：https://example.com/image_generated"

@tool
def text_to_speech_tool(text: str) -> str:
    """
    一个用于将文本转换为语音的工具。
    输入参数:
        - text (str): 你希望转换为语音的文本。
    """
    print(f"\n--- 正在调用文生语音工具 ---")
    print(f"输入文本: '{text}'")
    # 模拟语音生成过程
    return f"语音文件已根据文本 '{text}' 生成。你可以点击这里播放：https://example.com/audio_file.mp3"

@tool
def search_tool(query: str) -> str:
    """
    一个用于在互联网上进行搜索的工具。
    输入参数:
        - query (str): 你的搜索查询。
    """
    print(f"\n--- 正在调用搜索工具 ---")
    print(f"搜索查询: '{query}'")
    # 模拟搜索过程
    return f"搜索结果: 在互联网上找到了关于 '{query}' 的最新信息。"

@tool
def image_recognition_tool(image_url: str) -> str:
    """
    一个用于识别图片内容的工具。
    输入参数:
        - image_url (str): 图片的URL地址。
    """
    print(f"\n--- 正在调用图片识别工具 ---")
    print(f"图片URL: '{image_url}'")
    # 模拟图片识别过程
    return f"图片识别结果: 该图片似乎显示了一只正在睡觉的猫。"

# 将所有工具打包成一个列表
tools = [image_generation_tool, text_to_speech_tool, search_tool, image_recognition_tool]


# ----------------- 2. 初始化模型 -----------------
# 选择一个支持工具调用的模型。
# 这里使用 Ollama 模型作为示例。如果想使用 OpenAI，请确保设置了 OPENAI_API_KEY。
# ollama_model = ChatOllama(model="llama3")
# model = ollama_model.bind_tools(tools)
# 注意：你需要本地运行 `ollama run llama3`
# 如果使用 OpenAI，请确保环境变量 OPENAI_API_KEY 已设置
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
model_with_tools = model.bind_tools(tools)

# ----------------- 3. 构建 LangGraph 状态和节点 -----------------

# 定义图的状态
class AgentState(TypedDict):
    """
    一个简单的 LangGraph 状态，用于存储对话信息和工具调用。
    """
    messages: List[BaseMessage]

# 定义模型调用节点
def call_model(state: AgentState):
    """
    调用模型，并返回其响应。
    """
    messages = state['messages']
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}

# 定义工具调用节点
def call_tool(state: AgentState):
    """
    解析模型响应中的工具调用，并执行相应的工具。
    """
    last_message = state['messages'][-1]
    
    # 获取模型响应中的所有工具调用
    tool_calls = last_message.tool_calls
    if not tool_calls:
        # 如果模型没有调用工具，这通常不应该发生在这个节点
        print("警告: 模型没有返回工具调用。")
        return {"messages": []}

    tool_outputs = []
    # 遍历并执行所有工具调用
    for tool_call in tool_calls:
        tool_name = tool_call['name']
        tool_args = tool_call['args']
        
        # 根据工具名称查找并执行对应的函数
        tool_to_run = None
        for t in tools:
            if t.name == tool_name:
                tool_to_run = t
                break
        
        if tool_to_run:
            try:
                # 执行工具函数，传入参数
                output = tool_to_run.invoke(tool_args)
                tool_outputs.append(HumanMessage(content=f"工具输出: {output}"))
            except Exception as e:
                tool_outputs.append(HumanMessage(content=f"执行工具 '{tool_name}' 时出错: {e}"))
        else:
            tool_outputs.append(HumanMessage(content=f"未找到工具: '{tool_name}'"))
            
    # 将工具的输出作为新的消息添加到状态中，供模型继续处理
    return {"messages": tool_outputs}


# ----------------- 4. 构建 LangGraph 路由 -----------------

# 定义路由逻辑，根据模型输出决定下一步去哪里
def should_continue(state: AgentState):
    """
    如果模型调用了工具，则继续到 'call_tool' 节点；否则，对话结束。
    """
    last_message = state['messages'][-1]
    # 检查模型响应中是否包含工具调用
    if not last_message.tool_calls:
        # 如果没有工具调用，结束图的执行
        print("\n--- 模型已生成最终回复，对话结束 ---")
        return "end"
    else:
        # 如果有工具调用，继续到 call_tool 节点
        print("\n--- 模型正在调用工具... ---")
        return "continue"

# ----------------- 5. 组装 LangGraph 图 -----------------

# 建立一个状态图
workflow = StateGraph(AgentState)

# 添加节点
workflow.add_node("call_model", call_model)
workflow.add_node("call_tool", call_tool)

# 设置图的起点
workflow.set_entry_point("call_model")

# 添加条件边（路由）
workflow.add_conditional_edges(
    "call_model",       # 从 'call_model' 节点开始
    should_continue,    # 使用这个函数来决定下一步
    {
        "continue": "call_tool",  # 如果返回 "continue", 移动到 'call_tool'
        "end": END               # 如果返回 "end", 结束执行
    }
)

# 添加普通边
# 在 call_tool 节点执行完后，将结果返回给 call_model
workflow.add_edge('call_tool', 'call_model')

# 编译图
app = workflow.compile()

# ----------------- 6. 运行示例 -----------------
if __name__ == "__main__":
    print("Agent已启动。你可以输入指令，Agent会根据指令自动调用相应的工具。")
    print("输入 'exit' 退出程序。")

    while True:
        user_input = input("\n你: ")
        if user_input.lower() == 'exit':
            break

        # 准备初始状态
        initial_state = {"messages": [HumanMessage(content=user_input)]}
        
        # 调用 LangGraph
        final_state = app.invoke(initial_state)

        # 打印最终的回复
        final_message = final_state['messages'][-1]
        print("\nAgent:")
        print(final_message.content)
```
eof
---
### 代码使用说明

1.  **安装依赖**:
    ```bash
    pip install langchain langchain-openai langgraph
    ```

2.  **配置模型**:
    * **OpenAI**: 如果你使用 `ChatOpenAI`，请确保你已经安装了 `langchain-openai` 并设置了环境变量 `OPENAI_API_KEY`。
    * **Ollama**: 如果你选择使用本地的 `Ollama` 模型，请先安装 Ollama 并在终端运行 `ollama run llama3`（或者其他你喜欢的模型），然后将代码中的 `model` 变量切换为 `ChatOllama`。

3.  **运行脚本**:
    ```bash
    python tool_calling_demo.py
    
