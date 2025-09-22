FROM python:3.9-slim

WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install flask prometheus-client

# 复制应用代码
COPY app.py .

# 暴露端口
EXPOSE 5000

# 启动应用
CMD ["python", "app.py"]