#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LangGraph RAG系统演示
展示检索增强生成、向量搜索、知识库管理
"""

import os
import sys
import json
import time
import uuid
import asyncio
from typing import TypedDict, List, Dict, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime, timezone
import logging

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langgraph.runtime import Runtime
from langchain_core.embeddings import Embeddings
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


# ==================== 嵌入模型实现 ====================

class MockEmbeddings(Embeddings):
    """模拟嵌入模型（用于演示）"""
    
    def __init__(self, dimensions: int = 384):
        self.dimensions = dimensions
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """文档嵌入"""
        embeddings = []
        for text in texts:
            # 简单的基于词频的向量化
            words = text.lower().split()
            vector = [0.0] * self.dimensions
            
            for i, word in enumerate(words[:self.dimensions]):
                # 使用词的位置和长度生成向量
                vector[i] = (hash(word) % 1000) / 1000.0
            
            # 归一化
            norm = sum(x * x for x in vector) ** 0.5
            if norm > 0:
                vector = [x / norm for x in vector]
            
            embeddings.append(vector)
        
        return embeddings
    
    def embed_query(self, text: str) -> List[float]:
        """查询嵌入"""
        return self.embed_documents([text])[0]


# ==================== 知识库管理 ====================

@dataclass
class Document:
    """文档结构"""
    id: str
    title: str
    content: str
    source: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "source": self.source,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }


class KnowledgeBase:
    """知识库管理器"""
    
    def __init__(self, store: InMemoryStore, embeddings: Embeddings):
        self.store = store
        self.embeddings = embeddings
        self.documents: Dict[str, Document] = {}
    
    def add_document(self, document: Document) -> str:
        """添加文档到知识库"""
        # 存储文档元数据
        self.documents[document.id] = document
        self.store.put(
            ("documents",),
            document.id,
            document.to_dict()
        )
        
        # 创建嵌入并存储
        embeddings = self.embeddings.embed_documents([document.content])
        self.store.put(
            ("embeddings",),
            document.id,
            {
                "document_id": document.id,
                "embedding": embeddings[0],
                "content": document.content,
                "title": document.title,
                "source": document.source
            }
        )
        
        return document.id
    
    def search_documents(self, query: str, limit: int = 5, min_score: float = 0.0) -> List[Dict[str, Any]]:
        """搜索文档"""
        # 使用向量搜索
        results = self.store.search(
            ("embeddings",),
            query=query,
            limit=limit
        )
        
        # 过滤低分结果
        filtered_results = []
        for result in results:
            if result.score and result.score >= min_score:
                filtered_results.append({
                    "document_id": result.value["document_id"],
                    "title": result.value["title"],
                    "content": result.value["content"],
                    "source": result.value["source"],
                    "score": result.score
                })
        
        return filtered_results
    
    def get_document(self, document_id: str) -> Optional[Document]:
        """获取文档"""
        return self.documents.get(document_id)


# ==================== RAG状态定义 ====================

class RAGState(TypedDict):
    """RAG状态"""
    query: str
    retrieved_documents: List[Dict[str, Any]]
    context: str
    response: str
    metadata: Dict[str, Any]


# ==================== RAG图节点 ====================

# 全局知识库实例
_global_knowledge_base = None

def create_rag_graph():
    """创建RAG图"""
    
    def document_retrieval_node(state: RAGState, runtime: Runtime[Any]) -> RAGState:
        """文档检索节点"""
        global _global_knowledge_base
        query = state["query"]
        
        # 获取知识库
        if _global_knowledge_base is None:
            embeddings = MockEmbeddings()
            _global_knowledge_base = KnowledgeBase(runtime.store, embeddings)
        
        # 搜索相关文档
        retrieved_docs = _global_knowledge_base.search_documents(
            query=query,
            limit=5,
            min_score=0.3
        )
        
        state["retrieved_documents"] = retrieved_docs
        state["metadata"]["retrieval_count"] = len(retrieved_docs)
        
        return state
    
    def context_building_node(state: RAGState, runtime: Runtime[Any]) -> RAGState:
        """上下文构建节点"""
        retrieved_docs = state["retrieved_documents"]
        
        # 构建上下文
        context_parts = []
        for i, doc in enumerate(retrieved_docs, 1):
            context_parts.append(
                f"文档{i} (来源: {doc['source']}, 相关性: {doc['score']:.3f}):\n"
                f"{doc['content'][:200]}..."
            )
        
        context = "\n\n".join(context_parts)
        state["context"] = context
        state["metadata"]["context_length"] = len(context)
        
        return state
    
    def response_generation_node(state: RAGState, runtime: Runtime[Any]) -> RAGState:
        """响应生成节点"""
        query = state["query"]
        context = state["context"]
        retrieved_docs = state["retrieved_documents"]
        
        # 生成基于上下文的响应
        if retrieved_docs:
            # 基于检索到的文档生成响应
            response = f"基于知识库的回答:\n\n"
            response += f"问题: {query}\n\n"
            response += f"根据相关文档，我找到以下信息:\n\n"
            
            for i, doc in enumerate(retrieved_docs, 1):
                response += f"{i}. {doc['title']} (相关性: {doc['score']:.3f})\n"
                response += f"   {doc['content'][:150]}...\n\n"
            
            response += f"基于这些信息，我的回答是: 这是一个关于'{query}'的问题，"
            response += f"我在知识库中找到了{len(retrieved_docs)}个相关文档。"
        else:
            response = f"抱歉，我在知识库中没有找到关于'{query}'的相关信息。"
        
        state["response"] = response
        state["metadata"]["response_generated"] = True
        
        return state
    
    # 创建图
    graph = StateGraph(state_schema=RAGState)
    graph.add_node("document_retrieval", document_retrieval_node)
    graph.add_node("context_building", context_building_node)
    graph.add_node("response_generation", response_generation_node)
    
    graph.set_entry_point("document_retrieval")
    graph.add_edge("document_retrieval", "context_building")
    graph.add_edge("context_building", "response_generation")
    graph.add_edge("response_generation", END)
    
    return graph


# ==================== 知识库初始化 ====================

def initialize_knowledge_base(store: InMemoryStore, embeddings: Embeddings) -> KnowledgeBase:
    """初始化知识库"""
    kb = KnowledgeBase(store, embeddings)
    
    # 添加示例文档
    documents = [
        Document(
            id="doc_001",
            title="LangGraph基础概念",
            content="LangGraph是一个用于构建有状态多智能体应用的框架。它基于LangChain构建，提供了强大的图执行引擎和状态管理能力。LangGraph支持复杂的对话流程、记忆机制和智能体协作。",
            source="官方文档",
            metadata={"category": "framework", "difficulty": "beginner"}
        ),
        Document(
            id="doc_002",
            title="记忆机制实现",
            content="LangGraph的记忆机制通过checkpoint和store实现。checkpoint保存图执行状态，store提供持久化存储。支持短期记忆、长期记忆和向量搜索。记忆可以跨会话保持，支持复杂的上下文管理。",
            source="技术文档",
            metadata={"category": "memory", "difficulty": "intermediate"}
        ),
        Document(
            id="doc_003",
            title="RAG系统架构",
            content="RAG（检索增强生成）结合了信息检索和文本生成。系统首先从知识库中检索相关文档，然后基于检索到的信息生成回答。这种方法提高了回答的准确性和相关性。",
            source="AI论文",
            metadata={"category": "rag", "difficulty": "advanced"}
        ),
        Document(
            id="doc_004",
            title="向量搜索技术",
            content="向量搜索使用嵌入模型将文本转换为高维向量，然后通过计算向量间的相似度来找到相关文档。常用的相似度计算方法包括余弦相似度和欧几里得距离。",
            source="机器学习指南",
            metadata={"category": "vector_search", "difficulty": "intermediate"}
        ),
        Document(
            id="doc_005",
            title="多智能体协作",
            content="多智能体系统由多个专门的智能体组成，每个智能体负责特定的任务。智能体之间通过消息传递和状态共享进行协作，可以处理复杂的任务分解和并行执行。",
            source="系统架构文档",
            metadata={"category": "multi_agent", "difficulty": "advanced"}
        ),
        Document(
            id="doc_006",
            title="Python编程基础",
            content="Python是一种高级编程语言，具有简洁的语法和强大的功能。它广泛应用于数据科学、人工智能、Web开发等领域。Python支持面向对象编程和函数式编程。",
            source="编程教程",
            metadata={"category": "programming", "difficulty": "beginner"}
        ),
        Document(
            id="doc_007",
            title="机器学习算法",
            content="机器学习算法包括监督学习、无监督学习和强化学习。常用的算法有线性回归、决策树、神经网络、支持向量机等。选择合适的算法取决于数据特征和任务需求。",
            source="ML教程",
            metadata={"category": "ml", "difficulty": "intermediate"}
        ),
        Document(
            id="doc_008",
            title="深度学习框架",
            content="深度学习框架如TensorFlow、PyTorch、Keras等提供了构建和训练神经网络的工具。这些框架支持GPU加速、自动微分和模型部署，大大简化了深度学习应用的开发。",
            source="深度学习指南",
            metadata={"category": "deep_learning", "difficulty": "advanced"}
        )
    ]
    
    # 添加文档到知识库
    for doc in documents:
        kb.add_document(doc)
    
    return kb


# ==================== 演示函数 ====================

def demo_rag_system():
    """演示RAG系统"""
    print("🔍 RAG系统演示")
    print("=" * 60)
    
    # 创建存储和检查点
    store = InMemoryStore(
        index={
            "dims": 384,
            "embed": MockEmbeddings(384),
            "fields": ["content", "title"]
        }
    )
    checkpointer = InMemorySaver()
    
    # 初始化知识库
    embeddings = MockEmbeddings(384)
    knowledge_base = initialize_knowledge_base(store, embeddings)
    
    print(f"知识库初始化完成，包含 {len(knowledge_base.documents)} 个文档")
    
    # 创建图
    graph = create_rag_graph()
    compiled_graph = graph.compile(store=store, checkpointer=checkpointer)
    
    # 测试查询
    test_queries = [
        "什么是LangGraph？",
        "如何实现记忆机制？",
        "RAG系统如何工作？",
        "向量搜索的原理是什么？",
        "多智能体系统如何协作？",
        "Python编程有什么特点？",
        "机器学习有哪些算法？",
        "深度学习框架有哪些？"
    ]
    
    thread_id = "rag_thread_001"
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n第 {i} 个查询:")
        print(f"问题: {query}")
        print("-" * 40)
        
        # 创建状态
        state = RAGState(
            query=query,
            retrieved_documents=[],
            context="",
            response="",
            metadata={}
        )
        
        # 运行图
        result = compiled_graph.invoke(
            state,
            config={"configurable": {"thread_id": thread_id}}
        )
        
        print(f"检索到 {result['metadata']['retrieval_count']} 个相关文档")
        print(f"上下文长度: {result['metadata']['context_length']} 字符")
        print(f"回答: {result['response']}")
        
        # 显示检索到的文档
        if result["retrieved_documents"]:
            print("\n检索到的文档:")
            for j, doc in enumerate(result["retrieved_documents"], 1):
                print(f"  {j}. {doc['title']} (相关性: {doc['score']:.3f})")
                print(f"     来源: {doc['source']}")
                print(f"     内容: {doc['content'][:100]}...")
        
        print("=" * 60)


def demo_vector_search():
    """演示向量搜索"""
    print("\n🔍 向量搜索演示")
    print("=" * 60)
    
    # 创建存储
    store = InMemoryStore(
        index={
            "dims": 384,
            "embed": MockEmbeddings(384),
            "fields": ["content"]
        }
    )
    
    # 初始化知识库
    embeddings = MockEmbeddings(384)
    knowledge_base = initialize_knowledge_base(store, embeddings)
    
    # 测试不同的搜索查询
    search_queries = [
        ("LangGraph框架", "应该找到框架相关文档"),
        ("记忆和存储", "应该找到记忆机制文档"),
        ("检索生成", "应该找到RAG相关文档"),
        ("向量相似度", "应该找到向量搜索文档"),
        ("智能体协作", "应该找到多智能体文档"),
        ("编程语言", "应该找到Python相关文档"),
        ("学习算法", "应该找到机器学习文档"),
        ("神经网络", "应该找到深度学习文档")
    ]
    
    for query, expected in search_queries:
        print(f"\n搜索查询: {query}")
        print(f"预期结果: {expected}")
        
        results = knowledge_base.search_documents(query, limit=3, min_score=0.1)
        
        if results:
            print(f"找到 {len(results)} 个相关文档:")
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result['title']} (相似度: {result['score']:.3f})")
                print(f"     来源: {result['source']}")
        else:
            print("  未找到相关文档")
        
        print("-" * 40)


def demo_knowledge_base_management():
    """演示知识库管理"""
    print("\n📚 知识库管理演示")
    print("=" * 60)
    
    # 创建存储
    store = InMemoryStore(
        index={
            "dims": 384,
            "embed": MockEmbeddings(384),
            "fields": ["content", "title"]
        }
    )
    
    # 初始化知识库
    embeddings = MockEmbeddings(384)
    knowledge_base = initialize_knowledge_base(store, embeddings)
    
    print(f"知识库包含 {len(knowledge_base.documents)} 个文档")
    
    # 按类别统计文档
    categories = {}
    for doc in knowledge_base.documents.values():
        category = doc.metadata.get("category", "unknown")
        categories[category] = categories.get(category, 0) + 1
    
    print("\n按类别统计:")
    for category, count in categories.items():
        print(f"  {category}: {count} 个文档")
    
    # 按难度统计文档
    difficulties = {}
    for doc in knowledge_base.documents.values():
        difficulty = doc.metadata.get("difficulty", "unknown")
        difficulties[difficulty] = difficulties.get(difficulty, 0) + 1
    
    print("\n按难度统计:")
    for difficulty, count in difficulties.items():
        print(f"  {difficulty}: {count} 个文档")
    
    # 演示文档检索
    print("\n文档检索演示:")
    doc_id = "doc_001"
    doc = knowledge_base.get_document(doc_id)
    if doc:
        print(f"文档ID: {doc.id}")
        print(f"标题: {doc.title}")
        print(f"来源: {doc.source}")
        print(f"内容: {doc.content[:100]}...")
        print(f"元数据: {doc.metadata}")
    
    # 演示批量搜索
    print("\n批量搜索演示:")
    batch_queries = ["LangGraph", "记忆", "RAG", "向量"]
    for query in batch_queries:
        results = knowledge_base.search_documents(query, limit=2, min_score=0.1)
        print(f"查询 '{query}': 找到 {len(results)} 个文档")
        for result in results:
            print(f"  - {result['title']} (相似度: {result['score']:.3f})")


def main():
    """主函数"""
    print("🚀 LangGraph RAG系统演示")
    print("=" * 60)
    
    try:
        # 运行演示
        demo_rag_system()
        demo_vector_search()
        demo_knowledge_base_management()
        
        print("\n🎉 RAG系统演示完成！")
        print("\n💡 RAG系统特性总结:")
        print("1. 知识库管理: 支持文档的添加、存储和检索")
        print("2. 向量搜索: 使用嵌入模型进行语义相似度搜索")
        print("3. 检索增强: 基于检索到的文档生成准确回答")
        print("4. 上下文构建: 智能组合多个相关文档的信息")
        print("5. 响应生成: 基于检索到的知识生成高质量回答")
        print("6. 可扩展性: 支持大规模知识库和复杂查询")
        
    except Exception as e:
        print(f"\n❌ 演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
