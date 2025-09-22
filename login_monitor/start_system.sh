#!/bin/bash

echo "🚀 启动登录监控系统（包含 Prometheus + Grafana + 告警）"
echo ""

# 检查 Docker 是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker 未运行，请先启动 Docker"
    exit 1
fi

# 构建并启动所有服务
echo "📦 构建并启动服务..."
docker-compose up -d --build

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo ""
echo "📊 服务状态检查:"
docker-compose ps

echo ""
echo "🎯 服务访问地址:"
echo "• Flask 应用:     http://localhost:5000"
echo "• Prometheus:     http://localhost:9090"
echo "• Grafana:        http://localhost:3000 (admin/admin123)"
echo "• Alertmanager:   http://localhost:9093"
echo ""
echo "🔍 健康检查:"
echo "• 应用健康:       http://localhost:5000/health"
echo "• 应用指标:       http://localhost:5000/metrics"
echo ""
echo "✅ 系统启动完成！"
echo ""
echo "📝 快速测试命令:"
echo "python test_api.py"