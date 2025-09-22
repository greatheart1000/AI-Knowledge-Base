# Login Monitor 登录监控系统

一个基于 **Flask + Prometheus + Grafana + Alertmanager** 的完整登录监控告警系统，具备直方图分析、实时告警和可视化仪表盘功能。

## 📋 项目概述

### 🚀 新功能特性
- 🔐 **用户认证服务**：提供用户注册、登录、登出功能
- 📊 **实时监控**：使用 Prometheus 收集详细的业务和性能指标
- 📈 **直方图分析**：响应时间、登录尝试次数、密码强度分布等
- 🎯 **智能告警**：多级告警规则，覆盖性能、安全、业务异常
- 📱 **多渠道通知**：支持飞书、邮件等多种通知方式
- 🎨 **可视化仪表盘**：Grafana 仪表盘展示直方图和关键指标
- 🐳 **容器化部署**：使用 Docker Compose 一键启动所有服务
- 🔍 **健康检查**：应用健康状态监控和故障诊断

### 🏗️ 技术架构
```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   用户请求   │───▶│  Flask App   │───▶│  用户数据库  │
└─────────────┘    │              │    └─────────────┘
                   │ + 增强指标    │
                   └──────────────┘
                           │
                           ▼ /metrics (5s间隔)
                   ┌──────────────┐
                   │ Prometheus   │
                   │ + 多维度指标  │
                   └──────────────┘
                           │
                    ┌──────┴───────┐
                    ▼              ▼
            ┌──────────────┐ ┌──────────────┐
            │  Grafana     │ │ Alertmanager │
            │ + 直方图展示  │ │ + 分级告警   │
            └──────────────┘ └──────────────┘
                    │               │
                    ▼               ▼
            ┌──────────────┐ ┌──────────────┐
            │  可视化面板   │ │  飞书/邮件    │
            └──────────────┘ └──────────────┘
```

## 🚀 快速开始

### 环境要求
- Docker 20.10+
- Docker Compose 2.0+
- Python 3.7+ (可选，用于本地开发)

### 一键启动
```bash
# 克隆项目
git clone <repository-url>
cd login_monitor

# 一键启动所有服务
./start_system.sh

# 或者手动启动
docker-compose up -d
```

### 服务访问地址
| 服务 | 地址 | 用户名/密码 | 说明 |
|------|------|------|------|
| Flask 应用 | http://localhost:5000 | - | 主应用服务 |
| Prometheus | http://localhost:9090 | - | 监控数据查询 |
| **Grafana** | http://localhost:3000 | admin/admin123 | **直方图仪表盘** |
| Alertmanager | http://localhost:9093 | - | 告警管理 |

## 📡 API 接口

### 1. 用户注册
```http
POST /register
Content-Type: application/json

{
  "username": "用户名",
  "password": "密码"
}
```

**响应示例：**
```json
{
  "status": "created"  // 或 "exists"（用户已存在）
}
```

### 2. 用户登录
```http
POST /login
Content-Type: application/json

{
  "username": "用户名",
  "password": "密码"
}
```

**响应示例：**
```json
{
  "status": "ok"  // 或 "fail"（登录失败）
}
```

### 3. 监控指标
```http
GET /metrics
```

返回 Prometheus 格式的指标数据，包括：
- `login_total`: 登录请求计数（按状态码分类）
- `register_total`: 注册请求计数（按状态码分类）
- `request_duration_seconds`: 请求延迟分布

## 🧪 测试方法

### 方法一：增强版测试脚本（推荐）
```bash
# 运行增强版测试脚本，生成直方图数据
python test_api.py
```

测试脚本会自动执行：
- ✅ 系统健康检查
- ✅ 基本功能测试（注册、登录、登出）
- ✅ **直方图数据生成**（不同密码强度、登录模式）
- ✅ **并发负载测试**（模拟真实用户行为）
- ✅ **暴力破解模拟**（安全测试）
- ✅ 关键指标监控

### 方法二：一键启动脚本
```bash
# 启动完整系统
./start_system.sh

# 系统会自动检查服务状态并提供访问地址
```

### 方法三：使用 curl 命令
```bash
# 测试注册
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'

# 测试登录
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'

# 查看指标
curl http://localhost:5000/metrics
```

### 方法三：本地开发测试
```bash
# 安装依赖
pip install flask prometheus-client

# 运行应用
python app.py

# 应用将在 http://localhost:5000 启动
```

## 📊 监控告警与直方图分析

### 📈 增强监控指标
系统会自动收集以下关键指标：

| 指标名称 | 类型 | 说明 | 标签 | 直方图用途 |
|---------|------|------|------|----------|
| `login_total` | Counter | 登录请求总数 | `status`, `method` | QPS 分析 |
| `register_total` | Counter | 注册请求总数 | `status` | 新用户增长 |
| `request_duration_seconds` | **Histogram** | 请求延迟分布 | `method`, `endpoint` | **响应时间分位数** |
| `login_attempts_per_user` | **Histogram** | 用户登录尝试次数 | - | **安全风险分析** |
| `password_strength_score` | **Histogram** | 密码强度分布 | - | **密码质量评估** |
| `response_size_bytes` | **Histogram** | 响应大小分布 | `endpoint` | **性能优化** |
| `active_sessions_total` | Gauge | 活跃会话数 | - | 并发监控 |
| `error_total` | Counter | 错误计数 | `error_type` | 故障分析 |
| `concurrent_requests` | Gauge | 并发请求数 | - | 负载监控 |

### 🚨 智能告警规则
系统包含多级告警机制：

#### 🔴 严重告警 (Critical)
- **高 QPS 异常**: 登录+注册 QPS > 50 req/s
- **暴力破解检测**: 95% 用户登录尝试 > 10 次
- **服务不可用**: 应用停止响应

#### 🟡 警告级别 (Warning)
- **错误率过高**: 错误率 > 10%
- **响应时间过长**: P95 响应时间 > 1s
- **活跃会话过多**: 活跃会话 > 1000

#### 🟢 信息级别 (Info)
- **密码强度偏低**: P50 密码强度 < 2 分

### 📱 多渠道通知
告警会通过以下渠道发送：
- 🔔 **飞书群消息** (需配置 Webhook URL)
- 📧 **邮件通知** (可选配置)
- 🔗 **Webhook 集成** (自定义系统)

### 🎨 Grafana 直方图仪表盘

访问 **http://localhost:3000** （admin/admin123）查看直方图分析：

#### 📈 主要直方图面板
1. **响应时间直方图**
   - P50/P95/P99 分位数分析
   - 帮助识别性能瓶颈
   
2. **用户登录尝试次数分布**
   - 检测异常登录行为
   - 暴力破解警告
   
3. **密码强度分布直方图**
   - 用户密码安全性评估
   - 密码政策优化建议

#### 📄 使用步骤
1. 登录 Grafana: http://localhost:3000
2. 点击“登录监控系统 - 直方图分析”仪表盘
3. 运行 `python test_api.py` 生成测试数据
4. 观察直方图实时变化

### 🔧 自定义告警
编辑 `alertmanager.yml` 文件来配置通知渠道：
```yaml
receivers:
  - name: 'feishu'
    webhook_configs:
      - url: 'https://open.feishu.cn/open-apis/bot/v2/hook/your-webhook-url'
        send_resolved: true
```

## 📁 项目结构

```
login_monitor/
├── app.py                          # Flask 主应用 (增强版)
├── docker-compose.yml              # Docker 编排配置 (含 Grafana)
├── prometheus.yml                  # Prometheus 配置 (优化版)
├── rules.yml                      # 告警规则定义 (多级告警)
├── alertmanager.yml               # 告警管理配置 (分级通知)
├── Dockerfile                     # Docker 构建文件
├── requirements.txt               # Python 依赖
├── start_system.sh               # 一键启动脚本
├── test_api.py                   # 增强版测试脚本
├── grafana/                      # Grafana 配置目录
│   ├── provisioning/
│   │   ├── datasources/
│   │   │   └── prometheus.yml    # 数据源配置
│   │   └── dashboards/
│   │       └── dashboard.yml     # 仪表盘配置
│   └── dashboards/
│       └── login_monitor.json    # 直方图仪表盘定义
└── README.md                     # 项目说明文档
```

### 🔧 新增核心文件说明

#### `grafana/dashboards/login_monitor.json`
包含直方图可视化的完整仪表盘：
- 响应时间分位数直方图 (P50/P95/P99)
- 登录尝试次数分布直方图
- 密码强度分布直方图
- 实时错误率和 QPS 监控

#### `start_system.sh`
一键启动脚本：
- 自动检查 Docker 环境
- 构建并启动所有服务
- 提供服务访问地址

#### 增强版 `app.py`
新增功能：
- 会话管理和用户状态跟踪
- 暴力破解检测和防护
- 密码强度评估
- 详细的错误分类和监控
- 多维度直方图指标收集

#### `app.py`
Flask 应用主文件，包含：
- 用户注册和登录 API
- Prometheus 指标收集
- 内存数据库（生产环境需替换为真实数据库）

#### `prometheus.yml`
Prometheus 监控配置：
- 30秒抓取间隔
- 目标服务：Flask 应用（app:5000）

#### `rules.yml`
告警规则定义：
- 监控登录注册 QPS
- 阈值：3000 req/min
- 告警持续时间：1分钟

#### `alertmanager.yml`
告警管理配置：
- 告警分组和去重
- 通知渠道配置
- 告警恢复通知

## 🔧 配置说明

### 环境变量
可通过环境变量调整配置：

```bash
# Flask 应用配置
export FLASK_HOST=0.0.0.0
export FLASK_PORT=5000

# Prometheus 配置
export PROMETHEUS_PORT=9090

# Alertmanager 配置
export ALERTMANAGER_PORT=9093
```

### 生产环境部署
在生产环境中，建议进行以下调整：

1. **数据库**：替换内存数据库为 MySQL/PostgreSQL
2. **安全性**：添加 API 认证和授权
3. **高可用**：部署多个应用实例
4. **持久化**：配置 Prometheus 数据持久化
5. **告警渠道**：配置邮件、短信等多种通知方式

### 性能调优
- **Prometheus 抓取间隔**：根据业务需求调整 `scrape_interval`
- **告警阈值**：根据实际业务量调整 QPS 阈值
- **数据保留**：配置 Prometheus 数据保留策略

## 🐛 故障排查

### 常见问题

**Q: 服务启动失败**
```bash
# 检查端口占用
netstat -tulpn | grep :5000
netstat -tulpn | grep :9090

# 查看容器日志
docker-compose logs app
docker-compose logs prom
```

**Q: 告警未发送**
1. 检查 Prometheus 规则是否生效：http://localhost:9090/rules
2. 检查 Alertmanager 状态：http://localhost:9093
3. 验证 Webhook URL 配置

**Q: 指标数据异常**
```bash
# 检查指标接口
curl http://localhost:5000/metrics

# 查看 Prometheus targets
# 访问 http://localhost:9090/targets
```

### 日志查看
```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f app
docker-compose logs -f prom
docker-compose logs -f alert
```

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件至：[your-email@example.com]

---

**注意**：本项目仅用于演示目的，生产环境使用前请进行充分的安全评估和性能测试。