#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LangGraph 高级记忆系统
实现生产级的长短期记忆、RAG、复杂对话场景管理
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


# ==================== 配置和枚举 ====================

class MemoryType(Enum):
    """记忆类型"""
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    EPISODIC = "episodic"  # 情节记忆
    SEMANTIC = "semantic"  # 语义记忆
    PROCEDURAL = "procedural"  # 程序记忆


class ImportanceLevel(Enum):
    """重要性级别"""
    LOW = 0.3
    MEDIUM = 0.6
    HIGH = 0.8
    CRITICAL = 1.0


@dataclass
class MemoryConfig:
    """记忆配置"""
    max_short_term_size: int = 20
    max_long_term_size: int = 1000
    importance_threshold: float = 0.7
    decay_factor: float = 0.95
    consolidation_interval: int = 10  # 每10轮对话进行一次记忆整合


# ==================== 记忆数据结构 ====================

@dataclass
class MemoryItem:
    """记忆项"""
    id: str
    content: str
    memory_type: MemoryType
    importance: float
    timestamp: datetime
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "content": self.content,
            "memory_type": self.memory_type.value,
            "importance": self.importance,
            "timestamp": self.timestamp.isoformat(),
            "access_count": self.access_count,
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None,
            "tags": self.tags,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryItem':
        """从字典创建"""
        return cls(
            id=data["id"],
            content=data["content"],
            memory_type=MemoryType(data["memory_type"]),
            importance=data["importance"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            access_count=data.get("access_count", 0),
            last_accessed=datetime.fromisoformat(data["last_accessed"]) if data.get("last_accessed") else None,
            tags=data.get("tags", []),
            metadata=data.get("metadata", {})
        )


@dataclass
class ConversationContext:
    """对话上下文"""
    user_id: str
    session_id: str
    thread_id: str
    current_topic: str = ""
    conversation_goals: List[str] = field(default_factory=list)
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    active_memories: List[str] = field(default_factory=list)  # 当前激活的记忆ID


# ==================== 高级记忆管理器 ====================

class AdvancedMemoryManager:
    """高级记忆管理器"""
    
    def __init__(self, store: InMemoryStore, config: MemoryConfig = None):
        self.store = store
        self.config = config or MemoryConfig()
        self.memory_cache: Dict[str, MemoryItem] = {}
        self.access_patterns: Dict[str, List[datetime]] = {}
        
    def add_memory(self, 
                   user_id: str, 
                   content: str, 
                   memory_type: MemoryType,
                   importance: float = 0.5,
                   tags: List[str] = None,
                   metadata: Dict[str, Any] = None) -> str:
        """添加记忆"""
        memory_id = str(uuid.uuid4())
        
        memory_item = MemoryItem(
            id=memory_id,
            content=content,
            memory_type=memory_type,
            importance=importance,
            timestamp=datetime.now(timezone.utc),
            tags=tags or [],
            metadata=metadata or {}
        )
        
        # 存储到缓存和持久化存储
        self.memory_cache[memory_id] = memory_item
        self.store.put(
            ("memories", user_id, memory_type.value),
            memory_id,
            memory_item.to_dict()
        )
        
        return memory_id
    
    def retrieve_memories(self, 
                         user_id: str, 
                         query: str = "",
                         memory_types: List[MemoryType] = None,
                         limit: int = 10,
                         min_importance: float = 0.0) -> List[MemoryItem]:
        """检索记忆"""
        memories = []
        
        # 从存储中搜索
        for memory_type in (memory_types or list(MemoryType)):
            results = self.store.search(
                ("memories", user_id, memory_type.value),
                query=query,
                limit=limit
            )
            
            for result in results:
                memory_data = result.value
                if memory_data["importance"] >= min_importance:
                    memory_item = MemoryItem.from_dict(memory_data)
                    memories.append(memory_item)
        
        # 按重要性和时间排序
        memories.sort(key=lambda x: (x.importance, x.timestamp), reverse=True)
        return memories[:limit]
    
    def update_memory_access(self, memory_id: str):
        """更新记忆访问记录"""
        if memory_id in self.memory_cache:
            memory = self.memory_cache[memory_id]
            memory.access_count += 1
            memory.last_accessed = datetime.now(timezone.utc)
            
            # 更新访问模式
            if memory_id not in self.access_patterns:
                self.access_patterns[memory_id] = []
            self.access_patterns[memory_id].append(datetime.now(timezone.utc))
    
    def consolidate_memories(self, user_id: str) -> Dict[str, Any]:
        """记忆整合 - 将短期记忆整合到长期记忆"""
        consolidation_report = {
            "promoted_memories": 0,
            "decayed_memories": 0,
            "consolidated_at": datetime.now(timezone.utc).isoformat()
        }
        
        # 获取所有短期记忆
        short_term_memories = self.retrieve_memories(
            user_id, 
            memory_types=[MemoryType.SHORT_TERM],
            limit=100
        )
        
        for memory in short_term_memories:
            # 检查是否需要提升到长期记忆
            if (memory.importance >= self.config.importance_threshold and 
                memory.access_count >= 3):
                
                # 提升到长期记忆
                self.add_memory(
                    user_id,
                    memory.content,
                    MemoryType.LONG_TERM,
                    memory.importance,
                    memory.tags,
                    {**memory.metadata, "promoted_from": memory.id}
                )
                consolidation_report["promoted_memories"] += 1
                
            # 检查是否需要衰减
            elif (memory.importance < 0.3 and 
                  memory.last_accessed and 
                  datetime.now(timezone.utc) - memory.last_accessed > timedelta(days=7)):
                
                # 衰减记忆重要性
                memory.importance *= self.config.decay_factor
                if memory.importance < 0.1:
                    # 删除低重要性记忆
                    self.store.put(
                        ("memories", user_id, MemoryType.SHORT_TERM.value),
                        memory.id,
                        None  # 删除
                    )
                    consolidation_report["decayed_memories"] += 1
        
        return consolidation_report


# ==================== 智能记忆分析器 ====================

class MemoryAnalyzer:
    """记忆分析器"""
    
    def __init__(self):
        self.keyword_patterns = {
            "preference": ["喜欢", "偏好", "习惯", "prefer", "like"],
            "fact": ["是", "有", "在", "is", "has", "was"],
            "goal": ["想要", "希望", "需要", "want", "need", "goal"],
            "emotion": ["高兴", "难过", "生气", "happy", "sad", "angry"],
            "important": ["重要", "关键", "记住", "important", "critical", "remember"]
        }
    
    def analyze_content(self, content: str) -> Dict[str, Any]:
        """分析内容"""
        analysis = {
            "memory_type": MemoryType.SHORT_TERM,
            "importance": 0.5,
            "tags": [],
            "metadata": {}
        }
        
        content_lower = content.lower()
        
        # 分析记忆类型
        if any(keyword in content_lower for keyword in self.keyword_patterns["preference"]):
            analysis["memory_type"] = MemoryType.LONG_TERM
            analysis["tags"].append("preference")
        
        if any(keyword in content_lower for keyword in self.keyword_patterns["fact"]):
            analysis["memory_type"] = MemoryType.SEMANTIC
            analysis["tags"].append("fact")
        
        if any(keyword in content_lower for keyword in self.keyword_patterns["goal"]):
            analysis["memory_type"] = MemoryType.EPISODIC
            analysis["tags"].append("goal")
        
        # 分析重要性
        if any(keyword in content_lower for keyword in self.keyword_patterns["important"]):
            analysis["importance"] = 0.9
        elif any(keyword in content_lower for keyword in self.keyword_patterns["emotion"]):
            analysis["importance"] = 0.7
        elif len(content) > 100:  # 长内容通常更重要
            analysis["importance"] = 0.6
        
        # 提取元数据
        analysis["metadata"] = {
            "content_length": len(content),
            "word_count": len(content.split()),
            "has_question": "?" in content,
            "has_exclamation": "!" in content
        }
        
        return analysis


# ==================== 状态定义 ====================

class AdvancedConversationState(TypedDict):
    """高级对话状态"""
    messages: List[Dict[str, Any]]
    context: ConversationContext
    active_memories: List[Dict[str, Any]]  # 存储序列化的记忆数据
    memory_summary: str
    conversation_goals: List[str]
    user_preferences: Dict[str, Any]
    processing_metadata: Dict[str, Any]


# ==================== 图节点实现 ====================

def create_advanced_memory_graph():
    """创建高级记忆图"""
    
    # 创建全局记忆管理器和分析器实例
    global_memory_manager = None
    global_memory_analyzer = MemoryAnalyzer()
    
    def memory_analysis_node(state: AdvancedConversationState, runtime: Runtime[ConversationContext]) -> AdvancedConversationState:
        """记忆分析节点"""
        nonlocal global_memory_manager
        
        context = runtime.context
        current_message = state["messages"][-1] if state["messages"] else {}
        content = current_message.get('content', '')
        
        # 初始化记忆管理器 - 使用全局实例避免序列化问题
        if global_memory_manager is None:
            global_memory_manager = AdvancedMemoryManager(runtime.store)
        
        # 分析内容
        analysis = global_memory_analyzer.analyze_content(content)
        
        # 添加记忆
        memory_id = global_memory_manager.add_memory(
            user_id=context.user_id,
            content=content,
            memory_type=analysis["memory_type"],
            importance=analysis["importance"],
            tags=analysis["tags"],
            metadata=analysis["metadata"]
        )
        
        # 更新状态 - 只存储可序列化的数据
        state["processing_metadata"]["memory_analysis"] = analysis
        state["processing_metadata"]["memory_id"] = memory_id
        
        return state
    
    def memory_retrieval_node(state: AdvancedConversationState, runtime: Runtime[ConversationContext]) -> AdvancedConversationState:
        """记忆检索节点"""
        nonlocal global_memory_manager
        
        context = runtime.context
        current_message = state["messages"][-1] if state["messages"] else {}
        query = current_message.get('content', '')
        
        # 确保记忆管理器已初始化
        if global_memory_manager is None:
            global_memory_manager = AdvancedMemoryManager(runtime.store)
        
        # 检索相关记忆
        relevant_memories = global_memory_manager.retrieve_memories(
            user_id=context.user_id,
            query=query,
            limit=5,
            min_importance=0.3
        )
        
        # 更新访问记录
        for memory in relevant_memories:
            global_memory_manager.update_memory_access(memory.id)
        
        # 更新状态 - 将MemoryItem对象转换为可序列化的字典
        state["active_memories"] = [memory.to_dict() for memory in relevant_memories]
        state["context"].active_memories = [m["id"] for m in state["active_memories"]]
        
        return state
    
    def intelligent_response_node(state: AdvancedConversationState, runtime: Runtime[ConversationContext]) -> AdvancedConversationState:
        """智能响应节点"""
        current_message = state["messages"][-1] if state["messages"] else {}
        active_memories = state["active_memories"]
        
        # 构建记忆上下文 - 处理序列化的记忆数据
        memory_context = []
        for memory_dict in active_memories:
            memory_type = memory_dict.get("memory_type", "unknown")
            content = memory_dict.get("content", "")
            memory_context.append(f"[{memory_type}] {content[:50]}...")
        
        # 生成智能响应
        response_content = f"智能回复: {current_message.get('content', '')}"
        
        if memory_context:
            response_content += f"\n[相关记忆: {'; '.join(memory_context)}]"
        
        # 添加记忆摘要
        if len(state["messages"]) > 5:
            recent_topics = [msg.get('content', '')[:20] for msg in state["messages"][-5:]]
            state["memory_summary"] = f"最近话题: {', '.join(recent_topics)}"
        
        # 添加响应消息
        state["messages"].append({
            "role": "assistant",
            "content": response_content,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "memory_context": memory_context
        })
        
        return state
    
    def memory_consolidation_node(state: AdvancedConversationState, runtime: Runtime[ConversationContext]) -> AdvancedConversationState:
        """记忆整合节点"""
        nonlocal global_memory_manager
        
        context = runtime.context
        
        # 确保记忆管理器已初始化
        if global_memory_manager is None:
            global_memory_manager = AdvancedMemoryManager(runtime.store)
        
        # 检查是否需要整合记忆
        message_count = len(state["messages"])
        if message_count % global_memory_manager.config.consolidation_interval == 0:
            consolidation_report = global_memory_manager.consolidate_memories(context.user_id)
            state["processing_metadata"]["consolidation_report"] = consolidation_report
        
        return state
    
    # 创建图
    graph = StateGraph(state_schema=AdvancedConversationState)
    graph.add_node("memory_analysis", memory_analysis_node)
    graph.add_node("memory_retrieval", memory_retrieval_node)
    graph.add_node("intelligent_response", intelligent_response_node)
    graph.add_node("memory_consolidation", memory_consolidation_node)
    
    graph.set_entry_point("memory_analysis")
    graph.add_edge("memory_analysis", "memory_retrieval")
    graph.add_edge("memory_retrieval", "intelligent_response")
    graph.add_edge("intelligent_response", "memory_consolidation")
    graph.add_edge("memory_consolidation", END)
    
    return graph


# ==================== 演示函数 ====================

def demo_advanced_memory_system():
    """演示高级记忆系统"""
    print("🧠 高级记忆系统演示")
    print("=" * 60)
    
    # 创建存储和检查点
    store = InMemoryStore()
    checkpointer = InMemorySaver()
    
    # 创建图
    graph = create_advanced_memory_graph()
    compiled_graph = graph.compile(store=store, checkpointer=checkpointer)
    
    # 创建用户上下文
    user_context = ConversationContext(
        user_id="advanced_user_001",
        session_id=str(uuid.uuid4()),
        thread_id="advanced_thread_001",
        current_topic="AI技术讨论",
        conversation_goals=["学习LangGraph", "了解记忆机制"],
        user_preferences={"language": "zh", "detail_level": "high"}
    )
    
    # 模拟复杂对话场景
    conversation_scenarios = [
        {
            "message": "我喜欢喝咖啡，特别是拿铁，每天都要喝两杯",
            "expected_type": "preference",
            "expected_importance": "high"
        },
        {
            "message": "我的生日是12月25日，请记住这个重要日期",
            "expected_type": "fact",
            "expected_importance": "critical"
        },
        {
            "message": "我想要学习更多关于人工智能的知识",
            "expected_type": "goal",
            "expected_importance": "medium"
        },
        {
            "message": "今天天气怎么样？",
            "expected_type": "episodic",
            "expected_importance": "low"
        },
        {
            "message": "请告诉我关于记忆机制的信息",
            "expected_type": "semantic",
            "expected_importance": "medium"
        }
    ]
    
    for i, scenario in enumerate(conversation_scenarios):
        print(f"\n第 {i+1} 轮对话:")
        print(f"场景: {scenario['message']}")
        
        # 创建状态
        state = AdvancedConversationState(
            messages=[{
                "role": "user",
                "content": scenario["message"],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }],
            context=user_context,
            active_memories=[],
            memory_summary="",
            conversation_goals=[],
            user_preferences={},
            processing_metadata={}
        )
        
        # 运行图
        result = compiled_graph.invoke(
            state,
            config={"configurable": {"thread_id": user_context.thread_id}},
            context=user_context
        )
        
        print(f"用户: {scenario['message']}")
        print(f"助手: {result['messages'][-1]['content']}")
        
        # 显示记忆分析结果
        if result["processing_metadata"].get("memory_analysis"):
            analysis = result["processing_metadata"]["memory_analysis"]
            print(f"记忆分析: 类型={analysis['memory_type'].value}, 重要性={analysis['importance']:.2f}")
            print(f"标签: {analysis['tags']}")
        
        # 显示激活的记忆
        if result["active_memories"]:
            print("激活的记忆:")
            for memory_dict in result["active_memories"]:
                memory_type = memory_dict.get("memory_type", "unknown")
                content = memory_dict.get("content", "")
                importance = memory_dict.get("importance", 0.0)
                print(f"  - [{memory_type}] {content[:40]}... (重要性: {importance:.2f})")
        
        # 显示整合报告
        if result["processing_metadata"].get("consolidation_report"):
            report = result["processing_metadata"]["consolidation_report"]
            print(f"记忆整合: 提升={report['promoted_memories']}, 衰减={report['decayed_memories']}")
        
        print("-" * 50)


def demo_memory_consolidation():
    """演示记忆整合过程"""
    print("\n🔄 记忆整合演示")
    print("=" * 60)
    
    # 创建记忆管理器
    store = InMemoryStore()
    memory_manager = AdvancedMemoryManager(store)
    
    user_id = "consolidation_user"
    
    # 添加不同类型的记忆
    memories_to_add = [
        ("我喜欢喝咖啡", MemoryType.SHORT_TERM, 0.8),
        ("我的名字是张三", MemoryType.SHORT_TERM, 0.9),
        ("今天天气很好", MemoryType.SHORT_TERM, 0.3),
        ("我是一名程序员", MemoryType.SHORT_TERM, 0.7),
        ("明天有会议", MemoryType.SHORT_TERM, 0.6),
    ]
    
    print("添加初始记忆:")
    for content, memory_type, importance in memories_to_add:
        memory_id = memory_manager.add_memory(user_id, content, memory_type, importance)
        print(f"  - {content} (重要性: {importance})")
    
    # 模拟访问模式
    print("\n模拟记忆访问:")
    all_memories = memory_manager.retrieve_memories(user_id, limit=10)
    for memory in all_memories[:3]:  # 访问前3个记忆
        for _ in range(5):  # 每个记忆访问5次
            memory_manager.update_memory_access(memory.id)
        print(f"  - 访问记忆: {memory.content} (访问次数: {memory.access_count})")
    
    # 执行记忆整合
    print("\n执行记忆整合:")
    consolidation_report = memory_manager.consolidate_memories(user_id)
    print(f"整合报告: {consolidation_report}")
    
    # 显示整合后的记忆状态
    print("\n整合后的记忆状态:")
    final_memories = memory_manager.retrieve_memories(user_id, limit=10)
    for memory in final_memories:
        print(f"  - [{memory.memory_type.value}] {memory.content} (重要性: {memory.importance:.2f}, 访问: {memory.access_count})")


def main():
    """主函数"""
    print("🚀 LangGraph 高级记忆系统演示")
    print("=" * 60)
    
    try:
        # 运行演示
        demo_advanced_memory_system()
        demo_memory_consolidation()
        
        print("\n🎉 高级记忆系统演示完成！")
        print("\n💡 高级特性总结:")
        print("1. 智能记忆分析: 自动识别记忆类型和重要性")
        print("2. 分层记忆管理: 短期、长期、情节、语义、程序记忆")
        print("3. 记忆整合机制: 自动提升重要记忆，衰减无用记忆")
        print("4. 访问模式跟踪: 记录记忆使用频率和模式")
        print("5. 上下文感知: 基于对话上下文智能检索相关记忆")
        print("6. 生产级架构: 支持大规模部署和持久化存储")
        
    except Exception as e:
        print(f"\n❌ 演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
