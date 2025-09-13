#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LangGraph 复杂对话场景演示
展示多轮对话、上下文管理、状态持久化
"""

import os
import sys
import json
import time
import uuid
import asyncio
from typing import TypedDict, List, Dict, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
import logging

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langgraph.runtime import Runtime
from langchain_core.embeddings import Embeddings
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


# ==================== 对话状态和上下文 ====================

class ConversationPhase(Enum):
    """对话阶段"""
    GREETING = "greeting"
    TOPIC_DISCOVERY = "topic_discovery"
    DEEP_DISCUSSION = "deep_discussion"
    CLARIFICATION = "clarification"
    CONCLUSION = "conclusion"


class UserIntent(Enum):
    """用户意图"""
    QUESTION = "question"
    REQUEST = "request"
    CLARIFICATION = "clarification"
    CONFIRMATION = "confirmation"
    OBJECTION = "objection"
    COMPLAINT = "complaint"
    COMPLIMENT = "compliment"


@dataclass
class ConversationContext:
    """对话上下文"""
    user_id: str
    session_id: str
    thread_id: str
    current_phase: ConversationPhase
    conversation_history: List[Dict[str, Any]]
    user_profile: Dict[str, Any]
    active_topics: List[str]
    conversation_goals: List[str]
    emotional_state: str
    last_interaction: datetime
    interaction_count: int = 0


class ComplexConversationState(TypedDict):
    """复杂对话状态"""
    messages: List[Dict[str, Any]]
    context: ConversationContext
    current_intent: UserIntent
    conversation_phase: ConversationPhase
    active_memories: List[Dict[str, Any]]
    response_strategy: str
    metadata: Dict[str, Any]


# ==================== 意图识别器 ====================

class IntentRecognizer:
    """意图识别器"""
    
    def __init__(self):
        self.intent_patterns = {
            UserIntent.QUESTION: ["什么", "如何", "为什么", "怎么", "what", "how", "why", "?"],
            UserIntent.REQUEST: ["请", "帮我", "需要", "想要", "please", "help", "need", "want"],
            UserIntent.CLARIFICATION: ["澄清", "解释", "说明", "clarify", "explain", "elaborate"],
            UserIntent.CONFIRMATION: ["是的", "对的", "正确", "yes", "correct", "right", "确认"],
            UserIntent.OBJECTION: ["不对", "错误", "不同意", "no", "wrong", "disagree", "反对"],
            UserIntent.COMPLAINT: ["问题", "错误", "bug", "issue", "problem", "complaint"],
            UserIntent.COMPLIMENT: ["好", "棒", "优秀", "good", "great", "excellent", "amazing"]
        }
    
    def recognize_intent(self, message: str) -> UserIntent:
        """识别用户意图"""
        message_lower = message.lower()
        
        for intent, patterns in self.intent_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                return intent
        
        return UserIntent.QUESTION  # 默认意图


# ==================== 对话管理器 ====================

class ConversationManager:
    """对话管理器"""
    
    def __init__(self, store: InMemoryStore):
        self.store = store
        self.intent_recognizer = IntentRecognizer()
        self.conversation_patterns = {
            ConversationPhase.GREETING: self._handle_greeting,
            ConversationPhase.TOPIC_DISCOVERY: self._handle_topic_discovery,
            ConversationPhase.DEEP_DISCUSSION: self._handle_deep_discussion,
            ConversationPhase.CLARIFICATION: self._handle_clarification,
            ConversationPhase.CONCLUSION: self._handle_conclusion
        }
    
    def analyze_conversation(self, state: ComplexConversationState) -> Dict[str, Any]:
        """分析对话状态"""
        context = state["context"]
        messages = state["messages"]
        
        analysis = {
            "intent": self.intent_recognizer.recognize_intent(messages[-1]["content"]),
            "phase": self._determine_phase(context, messages),
            "emotional_tone": self._analyze_emotional_tone(messages),
            "topic_consistency": self._check_topic_consistency(messages),
            "conversation_flow": self._analyze_conversation_flow(messages)
        }
        
        return analysis
    
    def _determine_phase(self, context: ConversationContext, messages: List[Dict]) -> ConversationPhase:
        """确定对话阶段"""
        message_count = len(messages)
        
        if message_count <= 2:
            return ConversationPhase.GREETING
        elif message_count <= 5:
            return ConversationPhase.TOPIC_DISCOVERY
        elif message_count <= 10:
            return ConversationPhase.DEEP_DISCUSSION
        elif any("澄清" in msg["content"] or "clarify" in msg["content"].lower() for msg in messages[-3:]):
            return ConversationPhase.CLARIFICATION
        else:
            return ConversationPhase.CONCLUSION
    
    def _analyze_emotional_tone(self, messages: List[Dict]) -> str:
        """分析情感语调"""
        positive_words = ["好", "棒", "优秀", "满意", "喜欢", "good", "great", "excellent"]
        negative_words = ["不好", "糟糕", "问题", "错误", "bad", "terrible", "problem", "issue"]
        
        recent_messages = messages[-3:] if len(messages) >= 3 else messages
        content = " ".join([msg["content"] for msg in recent_messages]).lower()
        
        positive_count = sum(1 for word in positive_words if word in content)
        negative_count = sum(1 for word in negative_words if word in content)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def _check_topic_consistency(self, messages: List[Dict]) -> float:
        """检查话题一致性"""
        if len(messages) < 2:
            return 1.0
        
        # 简单的关键词重叠分析
        recent_topics = []
        for msg in messages[-5:]:
            words = set(msg["content"].lower().split())
            recent_topics.append(words)
        
        if len(recent_topics) < 2:
            return 1.0
        
        # 计算话题重叠度
        overlaps = []
        for i in range(len(recent_topics) - 1):
            overlap = len(recent_topics[i] & recent_topics[i + 1])
            total = len(recent_topics[i] | recent_topics[i + 1])
            if total > 0:
                overlaps.append(overlap / total)
        
        return sum(overlaps) / len(overlaps) if overlaps else 0.0
    
    def _analyze_conversation_flow(self, messages: List[Dict]) -> str:
        """分析对话流程"""
        if len(messages) < 3:
            return "starting"
        
        # 分析对话模式
        question_count = sum(1 for msg in messages[-5:] if "?" in msg["content"])
        if question_count >= 2:
            return "questioning"
        elif any("谢谢" in msg["content"] or "thank" in msg["content"].lower() for msg in messages[-2:]):
            return "concluding"
        else:
            return "discussing"
    
    def _handle_greeting(self, state: ComplexConversationState) -> str:
        """处理问候阶段"""
        return "friendly_greeting"
    
    def _handle_topic_discovery(self, state: ComplexConversationState) -> str:
        """处理话题发现阶段"""
        return "topic_exploration"
    
    def _handle_deep_discussion(self, state: ComplexConversationState) -> str:
        """处理深度讨论阶段"""
        return "detailed_response"
    
    def _handle_clarification(self, state: ComplexConversationState) -> str:
        """处理澄清阶段"""
        return "clarification_response"
    
    def _handle_conclusion(self, state: ComplexConversationState) -> str:
        """处理结论阶段"""
        return "conclusion_response"


# ==================== 记忆管理器 ====================

class ConversationMemoryManager:
    """对话记忆管理器"""
    
    def __init__(self, store: InMemoryStore):
        self.store = store
    
    def store_conversation_turn(self, user_id: str, turn_data: Dict[str, Any]):
        """存储对话轮次"""
        turn_id = str(uuid.uuid4())
        self.store.put(
            ("conversation_turns", user_id),
            turn_id,
            {
                **turn_data,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )
        return turn_id
    
    def retrieve_conversation_context(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """检索对话上下文"""
        results = self.store.search(
            ("conversation_turns", user_id),
            query="",
            limit=limit
        )
        return [result.value for result in results]
    
    def store_user_preference(self, user_id: str, preference: str, value: Any):
        """存储用户偏好"""
        self.store.put(
            ("user_preferences", user_id),
            preference,
            {
                "value": value,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )
    
    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """获取用户偏好"""
        results = self.store.search(
            ("user_preferences", user_id),
            query="",
            limit=100
        )
        return {result.key: result.value["value"] for result in results}


# ==================== 图节点实现 ====================

# 全局管理器实例
_global_conversation_manager = None
_global_memory_manager = None

def create_complex_conversation_graph():
    """创建复杂对话图"""
    
    def conversation_analysis_node(state: ComplexConversationState, runtime: Runtime[ConversationContext]) -> ComplexConversationState:
        """对话分析节点"""
        global _global_conversation_manager, _global_memory_manager
        
        # 初始化全局管理器
        if _global_conversation_manager is None:
            _global_conversation_manager = ConversationManager(runtime.store)
        if _global_memory_manager is None:
            _global_memory_manager = ConversationMemoryManager(runtime.store)
        
        # 获取管理器
        conversation_manager = _global_conversation_manager
        
        # 分析对话
        analysis = conversation_manager.analyze_conversation(state)
        
        # 更新状态
        state["current_intent"] = analysis["intent"]
        state["conversation_phase"] = analysis["phase"]
        state["metadata"]["analysis"] = analysis
        
        # 更新上下文（从状态中获取）
        context = state["context"]
        context.current_phase = analysis["phase"]
        context.interaction_count += 1
        context.last_interaction = datetime.now(timezone.utc)
        
        return state
    
    def memory_retrieval_node(state: ComplexConversationState, runtime: Runtime[ConversationContext]) -> ComplexConversationState:
        """记忆检索节点"""
        global _global_memory_manager
        
        # 从状态中获取上下文
        context = state["context"]
        
        # 获取记忆管理器
        memory_manager = _global_memory_manager
        
        # 检索对话历史
        conversation_history = memory_manager.retrieve_conversation_context(
            context.user_id, limit=5
        )
        
        # 检索用户偏好
        user_preferences = memory_manager.get_user_preferences(context.user_id)
        
        # 更新状态
        state["active_memories"] = conversation_history
        state["context"].user_profile.update(user_preferences)
        
        return state
    
    def response_strategy_node(state: ComplexConversationState, runtime: Runtime[ConversationContext]) -> ComplexConversationState:
        """响应策略节点"""
        global _global_conversation_manager
        
        # 从全局变量获取对话管理器
        conversation_manager = _global_conversation_manager
        phase = state["conversation_phase"]
        
        # 确定响应策略
        strategy = conversation_manager.conversation_patterns[phase](state)
        state["response_strategy"] = strategy
        
        return state
    
    def response_generation_node(state: ComplexConversationState, runtime: Runtime[ConversationContext]) -> ComplexConversationState:
        """响应生成节点"""
        # 从状态中获取上下文
        context = state["context"]
        current_message = state["messages"][-1]
        strategy = state["response_strategy"]
        analysis = state["metadata"]["analysis"]
        
        # 基于策略生成响应
        if strategy == "friendly_greeting":
            response = f"你好！很高兴见到你。我是你的AI助手，有什么可以帮助你的吗？"
        elif strategy == "topic_exploration":
            response = f"这是一个很有趣的话题。让我们深入探讨一下：{current_message['content']}"
        elif strategy == "detailed_response":
            response = f"基于我们的讨论，我认为：{current_message['content']}。你对此有什么看法？"
        elif strategy == "clarification_response":
            response = f"让我澄清一下：{current_message['content']}。这样解释清楚了吗？"
        elif strategy == "conclusion_response":
            response = f"总结一下我们的讨论：{current_message['content']}。还有其他问题吗？"
        else:
            response = f"我理解你的问题：{current_message['content']}。让我为你详细解答。"
        
        # 添加情感和个性化
        if analysis["emotional_tone"] == "positive":
            response += " 很高兴能帮助你！"
        elif analysis["emotional_tone"] == "negative":
            response += " 我理解你的担忧，让我们来解决这个问题。"
        
        # 添加响应消息
        state["messages"].append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "strategy": strategy,
            "phase": state["conversation_phase"].value
        })
        
        return state
    
    def memory_storage_node(state: ComplexConversationState, runtime: Runtime[ConversationContext]) -> ComplexConversationState:
        """记忆存储节点"""
        global _global_memory_manager
        
        # 从状态中获取上下文
        context = state["context"]
        current_message = state["messages"][-1]
        
        # 获取记忆管理器
        memory_manager = _global_memory_manager
        
        # 存储对话轮次
        turn_data = {
            "user_message": state["messages"][-2] if len(state["messages"]) >= 2 else {},
            "assistant_message": current_message,
            "intent": state["current_intent"].value,
            "phase": state["conversation_phase"].value,
            "strategy": state["response_strategy"],
            "analysis": state["metadata"]["analysis"]
        }
        
        memory_manager.store_conversation_turn(context.user_id, turn_data)
        
        # 存储重要信息
        if state["current_intent"] in [UserIntent.REQUEST, UserIntent.CONFIRMATION]:
            memory_manager.store_user_preference(
                context.user_id,
                f"preference_{len(state['messages'])}",
                current_message["content"]
            )
        
        return state
    
    # 创建图
    graph = StateGraph(state_schema=ComplexConversationState)
    graph.add_node("conversation_analysis", conversation_analysis_node)
    graph.add_node("memory_retrieval", memory_retrieval_node)
    graph.add_node("response_strategy", response_strategy_node)
    graph.add_node("response_generation", response_generation_node)
    graph.add_node("memory_storage", memory_storage_node)
    
    graph.set_entry_point("conversation_analysis")
    graph.add_edge("conversation_analysis", "memory_retrieval")
    graph.add_edge("memory_retrieval", "response_strategy")
    graph.add_edge("response_strategy", "response_generation")
    graph.add_edge("response_generation", "memory_storage")
    graph.add_edge("memory_storage", END)
    
    return graph


# ==================== 演示函数 ====================

def demo_complex_conversation():
    """演示复杂对话场景"""
    print("💬 复杂对话场景演示")
    print("=" * 60)
    
    # 创建存储和检查点
    store = InMemoryStore()
    checkpointer = InMemorySaver()
    
    # 创建图
    graph = create_complex_conversation_graph()
    compiled_graph = graph.compile(store=store, checkpointer=checkpointer)
    
    # 创建用户上下文
    user_context = ConversationContext(
        user_id="complex_user_001",
        session_id=str(uuid.uuid4()),
        thread_id="complex_thread_001",
        current_phase=ConversationPhase.GREETING,
        conversation_history=[],
        user_profile={"name": "张三", "interests": ["AI", "编程"]},
        active_topics=[],
        conversation_goals=["学习LangGraph", "了解记忆机制"],
        emotional_state="neutral",
        last_interaction=datetime.now(timezone.utc)
    )
    
    # 模拟复杂对话场景
    conversation_scenarios = [
        "你好，我想了解LangGraph",
        "它和LangChain有什么区别？",
        "记忆机制是如何工作的？",
        "能给我一个具体的例子吗？",
        "这个例子中的checkpoint是什么？",
        "如果我想在生产环境中使用，需要注意什么？",
        "性能方面有什么考虑？",
        "谢谢你的详细解释，我明白了"
    ]
    
    for i, user_message in enumerate(conversation_scenarios, 1):
        print(f"\n第 {i} 轮对话:")
        print(f"用户: {user_message}")
        
        # 创建状态
        state = ComplexConversationState(
            messages=[{
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }],
            context=user_context,
            current_intent=UserIntent.QUESTION,
            conversation_phase=ConversationPhase.GREETING,
            active_memories=[],
            response_strategy="",
            metadata={}
        )
        
        # 运行图
        result = compiled_graph.invoke(
            state,
            config={"configurable": {"thread_id": user_context.thread_id}},
            context=user_context
        )
        
        # 显示结果
        assistant_message = result["messages"][-1]
        print(f"助手: {assistant_message['content']}")
        
        # 显示分析结果
        analysis = result["metadata"]["analysis"]
        print(f"意图: {analysis['intent'].value}")
        print(f"阶段: {analysis['phase'].value}")
        print(f"情感: {analysis['emotional_tone']}")
        print(f"话题一致性: {analysis['topic_consistency']:.2f}")
        print(f"对话流程: {analysis['conversation_flow']}")
        print(f"响应策略: {result['response_strategy']}")
        
        # 显示激活的记忆
        if result["active_memories"]:
            print(f"激活记忆: {len(result['active_memories'])} 条")
        
        print("-" * 50)
        
        # 更新用户上下文
        user_context = result["context"]


def demo_conversation_memory():
    """演示对话记忆管理"""
    print("\n🧠 对话记忆管理演示")
    print("=" * 60)
    
    # 创建存储
    store = InMemoryStore()
    memory_manager = ConversationMemoryManager(store)
    
    user_id = "memory_user_001"
    
    # 模拟多轮对话记忆
    conversation_turns = [
        {
            "user_message": {"content": "我喜欢喝咖啡"},
            "assistant_message": {"content": "好的，我记住了你喜欢咖啡"},
            "intent": "preference",
            "phase": "topic_discovery"
        },
        {
            "user_message": {"content": "我是一名程序员"},
            "assistant_message": {"content": "很高兴认识你，程序员朋友！"},
            "intent": "information",
            "phase": "deep_discussion"
        },
        {
            "user_message": {"content": "我想学习AI技术"},
            "assistant_message": {"content": "AI技术很有趣，你想从哪个方面开始？"},
            "intent": "request",
            "phase": "deep_discussion"
        }
    ]
    
    print("存储对话轮次:")
    for i, turn in enumerate(conversation_turns, 1):
        turn_id = memory_manager.store_conversation_turn(user_id, turn)
        print(f"  轮次 {i}: {turn['user_message']['content']} -> {turn['assistant_message']['content']}")
    
    # 存储用户偏好
    print("\n存储用户偏好:")
    preferences = [
        ("drink", "咖啡"),
        ("profession", "程序员"),
        ("interest", "AI技术"),
        ("learning_style", "实践导向")
    ]
    
    for key, value in preferences:
        memory_manager.store_user_preference(user_id, key, value)
        print(f"  {key}: {value}")
    
    # 检索对话历史
    print("\n检索对话历史:")
    history = memory_manager.retrieve_conversation_context(user_id, limit=5)
    for i, turn in enumerate(history, 1):
        print(f"  历史 {i}: {turn['user_message']['content']} -> {turn['assistant_message']['content']}")
    
    # 检索用户偏好
    print("\n检索用户偏好:")
    user_prefs = memory_manager.get_user_preferences(user_id)
    for key, value in user_prefs.items():
        print(f"  {key}: {value}")


def demo_conversation_phases():
    """演示对话阶段管理"""
    print("\n🔄 对话阶段管理演示")
    print("=" * 60)
    
    # 创建对话管理器
    store = InMemoryStore()
    conversation_manager = ConversationManager(store)
    
    # 模拟不同阶段的对话
    phase_examples = {
        ConversationPhase.GREETING: [
            "你好",
            "很高兴见到你"
        ],
        ConversationPhase.TOPIC_DISCOVERY: [
            "我想了解LangGraph",
            "它有什么特点？"
        ],
        ConversationPhase.DEEP_DISCUSSION: [
            "记忆机制是如何实现的？",
            "能详细解释一下checkpoint的工作原理吗？"
        ],
        ConversationPhase.CLARIFICATION: [
            "我需要澄清一下这个概念",
            "能再解释一遍吗？"
        ],
        ConversationPhase.CONCLUSION: [
            "谢谢你的帮助",
            "我明白了，再见"
        ]
    }
    
    for phase, messages in phase_examples.items():
        print(f"\n{phase.value} 阶段:")
        for message in messages:
            # 创建模拟状态
            state = ComplexConversationState(
                messages=[{"role": "user", "content": message}],
                context=ConversationContext(
                    user_id="test_user",
                    session_id="test_session",
                    thread_id="test_thread",
                    current_phase=phase,
                    conversation_history=[],
                    user_profile={},
                    active_topics=[],
                    conversation_goals=[],
                    emotional_state="neutral",
                    last_interaction=datetime.now(timezone.utc)
                ),
                current_intent=UserIntent.QUESTION,
                conversation_phase=phase,
                active_memories=[],
                response_strategy="",
                metadata={}
            )
            
            analysis = conversation_manager.analyze_conversation(state)
            print(f"  消息: {message}")
            print(f"  识别意图: {analysis['intent'].value}")
            print(f"  情感语调: {analysis['emotional_tone']}")
            print(f"  话题一致性: {analysis['topic_consistency']:.2f}")


def main():
    """主函数"""
    print("🚀 LangGraph 复杂对话场景演示")
    print("=" * 60)
    
    try:
        # 运行演示
        demo_complex_conversation()
        demo_conversation_memory()
        demo_conversation_phases()
        
        print("\n🎉 复杂对话场景演示完成！")
        print("\n💡 复杂对话特性总结:")
        print("1. 意图识别: 自动识别用户意图和对话目标")
        print("2. 阶段管理: 智能管理对话的不同阶段")
        print("3. 情感分析: 分析用户情感状态和语调")
        print("4. 话题一致性: 跟踪对话话题的连贯性")
        print("5. 记忆管理: 持久化存储对话历史和用户偏好")
        print("6. 响应策略: 基于对话状态选择最佳响应策略")
        print("7. 上下文感知: 基于历史对话提供个性化响应")
        print("8. 状态持久化: 支持跨会话的状态保持")
        
    except Exception as e:
        print(f"\n❌ 演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
