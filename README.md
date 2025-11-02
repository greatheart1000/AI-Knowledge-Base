# AI Knowledge Base

一个集成了 LangGraph、RAG 系统、高级记忆管理和图像分类等多种 AI 技术的知识库项目。

## 📋 项目概述

本项目包含多个 AI 相关的演示和实用工具，主要包括：
- **LangGraph 工作流系统**：复杂对话场景、工具调用、状态管理
- **RAG 系统**：检索增强生成、向量搜索、知识库管理
- **高级记忆系统**：短期/长期记忆、记忆整合、访问模式跟踪
- **图像分类模型**：ResNet 模型训练和批量推理
- **数据处理工具**：数据创建、清洗、转换
- **分布式任务处理**：Kafka + Celery 任务队列

## 🚀 主要功能模块

### 1. LangGraph 工作流系统

#### 1.1 RAG 系统演示 (`rag_system_demo.py`)
- 知识库管理和文档检索
- 向量搜索和语义相似度匹配
- 基于检索结果的响应生成
- 上下文构建和组合

**主要特性：**
- 文档嵌入和向量化
- 多文档上下文组合
- 相关性评分和过滤

**运行示例：**
```bash
python rag_system_demo.py
```

#### 1.2 工具调用演示 (`tool_calling_demo.py`)
- 自动工具调用机制
- 支持多种工具（图像生成、文本转语音、搜索、图像识别）
- 条件路由和工具选择

**运行示例：**
```bash
python tool_calling_demo.py
```

#### 1.3 LangGraph 基础工作流 (`langgraph.py`)
- 规划节点：判断是否需要检索
- RAG 节点：从向量数据库检索文档
- 生成节点：结合检索结果生成答案
- 反思节点：评估答案质量
- 人工介入：处理复杂场景

**运行示例：**
```bash
python langgraph.py
```

#### 1.4 高级记忆系统 (`advanced_memory_system.py` / `production_memory_system.py`)
- **记忆类型**：短期记忆、长期记忆、情节记忆、语义记忆、程序记忆
- **智能记忆分析**：自动识别记忆类型和重要性
- **记忆整合机制**：自动提升重要记忆，衰减无用记忆
- **访问模式跟踪**：记录记忆使用频率和模式
- **上下文感知检索**：基于对话上下文智能检索相关记忆

**主要功能：**
- `MemoryAnalyzer`：分析内容并确定记忆类型和重要性
- `AdvancedMemoryManager`：管理记忆的添加、检索、更新
- `consolidate_memories`：记忆整合和衰减机制

**运行示例：**
```bash
python advanced_memory_system.py
# 或
python production_memory_system.py
```

#### 1.5 复杂对话场景 (`complex_conversation_demo.py`)
- 意图识别：自动识别用户意图（问题、请求、确认等）
- 阶段管理：管理对话的不同阶段（问候、话题发现、深度讨论等）
- 情感分析：分析用户情感状态和语调
- 话题一致性：跟踪对话话题的连贯性
- 记忆管理：持久化存储对话历史和用户偏好
- 响应策略：基于对话状态选择最佳响应策略

**运行示例：**
```bash
python complex_conversation_demo.py
```

### 2. 图像分类模型

#### 2.1 模型训练 (`train.py`)
- 使用 ResNet 架构（ResNet34/ResNet50/ResNet101）
- 支持多 GPU 并行训练
- 数据增强和预处理
- 训练过程监控和最佳模型保存

**主要功能：**
- 数据加载和预处理
- 模型训练和验证
- 类别索引生成
- 最佳模型自动保存

**配置说明：**
- 修改 `image_path` 指定数据路径
- 调整 `batch_size`、`epochs`、`lr` 等超参数
- 选择 ResNet 架构（resnet34/resnet50/resnet101）

**运行示例：**
```bash
python train.py
```

#### 2.2 批量推理 (`batch_infer.py`)
- 批量处理图像分类
- 支持 CSV 元数据输入
- 预测结果输出和正确率统计

**运行示例：**
```bash
python batch_infer.py
```

### 3. 数据处理工具

#### 3.1 数据创建和处理
- `create_data.py`：创建训练数据
- `create_COT_data.py`：创建 Chain-of-Thought 数据
- `select_test_data.py`：选择测试数据
- `batch_download_by_point_name.py`：按点位名称批量下载
- `clean_broken_images.py`：清理损坏的图像文件

### 4. 数据库操作

- `create_postgresql_tables.py`：创建 PostgreSQL 表结构
- `create_pogesql_table.py`：PostgreSQL 表创建工具
- `insert_embeding.py`：插入嵌入向量数据

### 5. 分布式任务处理

详细配置和使用说明请参考 [`kafka_celery.md`](kafka_celery.md)

- Kafka 作为消息代理
- Celery 作为任务队列
- 支持异步任务处理
- 分布式爬虫、图像处理、日志分析等应用场景

**主要文件：**
- `kafka_celery_worker_producer.py`：Kafka + Celery 工作节点和生产者

## 📦 环境要求

### 基础依赖
- Python 3.8+
- PyTorch（用于图像分类）
- LangChain / LangGraph（用于工作流系统）
- 其他依赖见具体模块

### 安装依赖

```bash
# 基础依赖
pip install torch torchvision pillow pandas

# LangGraph 相关
pip install langchain langchain-openai langgraph langchain-core

# 数据处理
pip install pandas openpyxl

# 数据库（如需要）
pip install psycopg2-binary

# Kafka + Celery（如需要）
pip install celery kafka-python
```

## 🛠️ 使用指南

### LangGraph 系统

1. **配置 API Key**（如使用 OpenAI）：
   ```bash
   export OPENAI_API_KEY="your-api-key"
   ```

2. **运行演示**：
   ```bash
   # RAG 系统
   python rag_system_demo.py
   
   # 工具调用
   python tool_calling_demo.py
   
   # 高级记忆系统
   python advanced_memory_system.py
   
   # 复杂对话场景
   python complex_conversation_demo.py
   ```

### 图像分类模型

1. **准备数据**：
   - 组织图像数据到 `train/` 和 `val/` 目录
   - 每个类别一个文件夹

2. **训练模型**：
   ```bash
   python train.py
   ```

3. **批量推理**：
   ```bash
   python batch_infer.py
   ```

### 数据处理

根据具体需求运行相应的数据处理脚本：
```bash
python create_data.py
python create_COT_data.py
# ... 其他数据处理脚本
```

## 📁 项目结构

```
AI-Knowledge-Base/
├── README.md                          # 项目说明文档
├── LICENSE                            # 许可证文件
│
├── # LangGraph 系统
├── rag_system_demo.py                 # RAG 系统演示
├── tool_calling_demo.py               # 工具调用演示
├── langgraph.py                       # LangGraph 基础工作流
├── advanced_memory_system.py          # 高级记忆系统
├── production_memory_system.py        # 生产级记忆系统
├── complex_conversation_demo.py       # 复杂对话场景
│
├── # 图像分类
├── train.py                           # 模型训练
├── batch_infer.py                     # 批量推理
├── batch_predict.py                   # 批量预测
│
├── # 数据处理
├── create_data.py                     # 创建训练数据
├── create_COT_data.py                 # 创建 COT 数据
├── select_test_data.py                # 选择测试数据
├── batch_download_by_point_name.py    # 批量下载
├── clean_broken_images.py             # 清理损坏图像
│
├── # 数据库
├── create_postgresql_tables.py        # 创建 PostgreSQL 表
├── create_pogesql_table.py            # PostgreSQL 工具
├── insert_embeding.py                 # 插入嵌入向量
│
├── # 分布式任务
├── kafka_celery_worker_producer.py   # Kafka + Celery 工具
├── kafka_celery.md                    # Kafka + Celery 文档
│
└── # 其他
├── class2name.py                      # 类别名称转换
├── cot0611.py                         # COT 数据处理
├── AI面试题.md                         # AI 面试题集合
└── test_texts.jsonl                   # 测试文本数据
```

## 🔧 配置说明

### LangGraph 配置

- **模型选择**：支持 OpenAI GPT 模型或本地 Ollama 模型
- **存储**：默认使用 InMemoryStore（可替换为持久化存储）
- **检查点**：使用 InMemorySaver（可替换为数据库检查点）

### 图像分类配置

在 `train.py` 中配置：
- `image_path`：数据路径
- `batch_size`：批次大小
- `epochs`：训练轮数
- `lr`：学习率
- 模型架构：resnet34/resnet50/resnet101

## 💡 核心特性

### LangGraph 系统特性

1. **状态管理**：完整的对话状态跟踪和管理
2. **记忆系统**：多层次的记忆管理和整合机制
3. **工具调用**：自动化的工具选择和调用
4. **RAG 集成**：检索增强生成能力
5. **意图识别**：智能识别用户意图和对话阶段
6. **情感分析**：分析用户情感状态

### 图像分类特性

1. **多架构支持**：ResNet34/50/101
2. **数据增强**：随机裁剪、翻转、归一化
3. **多 GPU 支持**：自动并行训练
4. **模型保存**：自动保存最佳模型

## 🐛 故障排查

### LangGraph 相关

- **API Key 错误**：确保设置了正确的 `OPENAI_API_KEY`
- **导入错误**：确保安装了所有必需的依赖包
- **存储错误**：检查存储配置和路径

### 图像分类相关

- **CUDA 错误**：确保安装了正确版本的 PyTorch 和 CUDA
- **数据路径错误**：检查数据路径和文件结构
- **模型权重错误**：确保模型权重文件存在且格式正确

## 📝 注意事项

1. **API 密钥**：使用 OpenAI API 时需要设置环境变量
2. **数据路径**：根据实际环境修改数据路径
3. **模型权重**：训练前可能需要预训练权重文件
4. **存储空间**：大量数据处理需要足够的存储空间

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

详见 [LICENSE](LICENSE) 文件

## 🔗 相关文档

- [Kafka + Celery 使用指南](kafka_celery.md)
- [AI 面试题集合](AI面试题.md)

## 📧 联系方式

如有问题或建议，请通过 Issue 反馈。

---

**注意**：本项目为学习和演示用途，生产环境使用前请进行充分测试和优化。