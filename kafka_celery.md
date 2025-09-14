详细当前的 Kafka + Celery 配置、安装步骤、运行流程以及相关示例。这将帮助你或他人快速上手你的项目。
---

```markdown
# Kafka + Celery 配置与使用指南

本项目展示了一个使用 Kafka 作为消息代理和 Celery 作为任务队列的分布式任务处理系统。以下是配置、安装和运行的详细步骤，以及一些实际应用的示例。

## 环境要求

- **操作系统**: Linux (WSL2 推荐, 如 Ubuntu)
- **Python**: 3.8 或以上
- **Kafka**: 2.13-4.1.0
- **Celery**: 5.5.3 或以上

## 安装步骤

### 1. 安装 Kafka
- 下载 Kafka 2.13-4.1.0：
  ```bash
  wget https://archive.apache.org/dist/kafka/2.13-4.1.0/kafka_2.13-4.1.0.tgz
  tar -xzf kafka_2.13-4.1.0.tgz
  mv kafka_2.13-4.1.0 /mnt/d/software/
  ```
- 确保 Java 环境已安装（Kafka 依赖 Java 8 或以上）：
  ```bash
  java -version
  ```

### 2. 配置 Kafka (Kraft 模式)
- 进入 Kafka 目录：
  ```bash
  cd /mnt/d/software/kafka_2.13-4.1.0/
  ```
- 生成 Cluster ID 并格式化存储：
  ```bash
  CLUSTER_ID=$(./bin/kafka-storage.sh random-uuid)
  echo $CLUSTER_ID
  mkdir -p config/kraft
  cp config/server.properties config/kraft/server.properties
  ```
- 编辑 `config/kraft/server.properties`，使用以下内容：
  ```properties
  process.roles=broker,controller
  node.id=1
  controller.quorum.voters=1@localhost:9093
  listeners=PLAINTEXT://:9092,CONTROLLER://:9093
  inter.broker.listener.name=PLAINTEXT
  advertised.listeners=PLAINTEXT://localhost:9092,CONTROLLER://localhost:9093
  controller.listener.names=CONTROLLER
  listener.security.protocol.map=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
  log.dirs=/tmp/kraft-combined-logs
  num.network.threads=3
  num.io.threads=8
  socket.send.buffer.bytes=102400
  socket.receive.buffer.bytes=102400
  socket.request.max.bytes=104857600
  num.partitions=1
  num.recovery.threads.per.data.dir=1
  offsets.topic.replication.factor=1
  log.retention.hours=168
  log.segment.bytes=1073741824
  log.retention.check.interval.ms=300000
  ```
- 格式化并启动 Kafka：
  ```bash
  ./bin/kafka-storage.sh format --cluster-id $CLUSTER_ID --config ./config/kraft/server.properties
  ./bin/kafka-server-start.sh ./config/kraft/server.properties
  ```

### 3. 安装 Python 依赖
- 进入项目目录：
  ```bash
  cd /mnt/d/project/langgraph/libs/multi_agent_system/
  ```
- 创建虚拟环境（可选但推荐）：
  ```bash
  python -m venv venv
  source venv/bin/activate
  ```
- 安装依赖：
  ```bash
  pip install celery kafka-python Pillow requests
  ```

## 项目结构
- `worker.py`: 定义 Celery 应用和任务逻辑。
- `producer.py`: 发送任务到 Celery。

## 运行步骤

### 1. 启动 Celery Worker
- 在项目目录下运行：
  ```bash
  celery -A worker worker --loglevel=info
  ```
- 预期输出：
  ```
  Celery worker 已准备就绪，正在监听任务...
  [2025-09-14 16:00:38,163: INFO/MainProcess] celery@Greatheart12san ready.
  ```

### 2. 运行 Producer
- 在新终端中运行：
  ```bash
  python producer.py
  ```
- 预期输出：
  ```
  正在发送任务到 Celery...
  任务已发送，任务ID: <some-uuid>
  任务结果已接收: 8
  ```

### 3. 验证
- 检查 Worker 日志，确保任务（如 `add`）被接收和执行。
- 确认 Producer 接收到结果。

## 任务示例

### 基本任务：加法
- **任务**: `worker.add`
- **功能**: 计算两个数的和。
- **代码**: 已包含在 `worker.py` 中。

### 实际应用场景

#### 1. 异步邮件发送
- **任务**: `worker.send_email`
- **功能**: 异步发送邮件。
- **使用**:
  - 更新 `worker.py` 和 `producer.py` 中的邮件配置。
  - 运行 Producer 发送邮件任务。
- **注意**: 替换 `your_email@example.com` 和 `your_password`。

#### 2. 数据处理管道
- **任务**: `worker.process_data`
- **功能**: 清洗 JSON 数据并保存。
- **使用**: 发送 JSON 字符串，Worker 返回处理结果。

#### 3. 定时任务 (数据备份)
- **任务**: `worker.backup_data`
- **功能**: 每 10 秒备份数据到文件。
- **使用**: 启动 Worker with Beat：
  ```bash
  celery -A worker worker --loglevel=info --beat
  ```

#### 4. 实时日志分析
- **任务**: `worker.analyze_logs`
- **功能**: 分析日志，检测错误并触发警报。
- **使用**: 发送日志 JSON，Worker 返回警报状态。

#### 5. 图像处理队列
- **任务**: `worker.process_image`
- **功能**: 调整图片大小并添加水印。
- **使用**: 提供图片路径，Worker 生成处理结果。
- **依赖**: 安装 `Pillow`。

#### 6. 分布式爬虫
- **任务**: `worker.crawl_url`
- **功能**: 异步抓取网页内容。
- **使用**: 发送 URL 列表，Worker 返回内容预览。
- **依赖**: 安装 `requests`。

## 配置文件
- **Kafka**: `config/kraft/server.properties`（见上文）。
- **Celery**: 定义在 `worker.py` 中，broker 为 `kafka://localhost:9092`，backend 为 `rpc://`。

## 故障排查
- **Kafka 未运行**: 检查 `kafka-server-start.sh` 输出，确认 `9092` 端口可用。
- **Celery 错误**: 确保依赖安装完整，检查日志级别（`--loglevel=debug`）。
- **路径问题**: 确认 `worker.py` 和 `producer.py` 在正确目录。

## 扩展建议
- **结果后端**: 替换 `rpc://` 为 Redis (`redis://localhost:6379/0`)。
- **并发优化**: 调整 `--concurrency` 参数。
- **监控**: 使用 `--events` 启用任务监控。

## 贡献
欢迎提出改进建议或添加新任务！

---
```

---

### 使用说明
1. **保存文件**：将上述内容保存为 `README.md`，放置在 `/mnt/d/project/langgraph/libs/multi_agent_system/` 目录下。
2. **调整路径**：根据你的实际文件路径（例如 `worker.py` 和 `producer.py` 所在目录）更新 `README.md` 中的路径。
3. **补充细节**：如果有特定需求（例如数据库配置或更多任务），可以告诉我，我会补充。

这个 `README.md` 提供了全面的指导，涵盖安装、运行和扩展。试试看吧！有问题随时告诉我！
