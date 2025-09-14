from celery import Celery

# 定义一个 Celery 实例
# 这里的配置需要和 worker.py 中的配置一致
app = Celery('tasks',
             broker='kafka://localhost:9092',
             backend='rpc://')

if __name__ == "__main__":
    print("正在发送任务到 Celery...")

    # 异步发送任务
    result = app.send_task('worker.add', args=[5, 3])
    print(f"任务已发送，任务ID: {result.id}")

    # 获取任务结果（阻塞式）
    # 在实际应用中，通常不会立即获取，而是通过回调或状态查询
    try:
        task_result = result.get(timeout=10)
        print(f"任务结果已接收: {task_result}")
    except Exception as e:
        print(f"获取任务结果时出错或超时: {e}")
from celery import Celery

# 定义一个 Celery 实例
# 这里的配置需要和 worker.py 中的配置一致
app = Celery('tasks',
             broker='kafka://localhost:9092',
             backend='rpc://')

if __name__ == "__main__":
    print("正在发送任务到 Celery...")

    # 异步发送任务
    result = app.send_task('worker.add', args=[5, 3])
    print(f"任务已发送，任务ID: {result.id}")

    # 获取任务结果（阻塞式）
    # 在实际应用中，通常不会立即获取，而是通过回调或状态查询
    try:
        task_result = result.get(timeout=10)
        print(f"任务结果已接收: {task_result}")
    except Exception as e:
        print(f"获取任务结果时出错或超时: {e}")

producer.py
==================================================
==================================================
下面的是worker.py

from celery import Celery
from celery.signals import worker_ready
from celery.app.task import Task
import time

# 定义一个 Celery 实例
# broker_url 指向你的 Kafka 代理
# backend_url 用于存储任务结果，这里我们使用一个简单的内存后端
app = Celery('tasks',
             broker='kafka://localhost:9092',
             backend='rpc://')

# 禁用任务结果序列化，这里是为了简单起见
app.conf.accept_content = ['json', 'application/json']
app.conf.result_serializer = 'json'

# 定义一个简单的任务
@app.task(bind=True)
def add(self: Task, x: int, y: int) -> int:
    """
    一个简单的加法任务，用于演示。
    """
    print(f"正在执行任务 {self.request.id}: {x} + {y}")
    time.sleep(2)  # 模拟耗时操作
    result = x + y
    print(f"任务 {self.request.id} 完成，结果是: {result}")
    return result

# 确保 Celery worker 准备就绪
@worker_ready.connect
def on_worker_ready(**kwargs):
    print("Celery worker 已准备就绪，正在监听任务...")

