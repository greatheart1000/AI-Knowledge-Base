#!/usr/bin/env python3
"""
增强版 API 测试脚本 - 包含直方图数据生成
"""
import requests
import json
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://localhost:5000"

def test_register(username, password):
    """测试注册接口"""
    url = f"{BASE_URL}/register"
    data = {"username": username, "password": password}
    
    response = requests.post(url, json=data)
    return response

def test_login(username, password):
    """测试登录接口"""
    url = f"{BASE_URL}/login"
    data = {"username": username, "password": password}
    
    response = requests.post(url, json=data)
    return response

def test_logout(session_id):
    """测试登出接口"""
    url = f"{BASE_URL}/logout"
    data = {"session_id": session_id}
    
    response = requests.post(url, json=data)
    return response

def test_health():
    """测试健康检查接口"""
    url = f"{BASE_URL}/health"
    response = requests.get(url)
    return response

def test_metrics():
    """测试指标接口"""
    url = f"{BASE_URL}/metrics"
    response = requests.get(url)
    return response

def generate_histogram_data():
    """生成用于直方图分析的测试数据"""
    print("\n🔥 开始生成直方图测试数据...")
    
    # 创建不同强度的密码
    passwords = {
        "weak": ["123", "abc", "password"],
        "medium": ["pass123", "hello2023", "user456"],
        "strong": ["MyStr0ng!Pass", "SecurePwd2023!", "C0mpl3x@Pass"]
    }
    
    users_created = []
    
    # 注册用户（不同密码强度）
    for strength, pwd_list in passwords.items():
        for i, pwd in enumerate(pwd_list):
            username = f"{strength}_user_{i}"
            response = test_register(username, pwd)
            if response.status_code == 200:
                users_created.append((username, pwd))
                print(f"  ✅ 注册 {strength} 用户: {username}")
    
    # 模拟不同的登录行为模式
    print("\n📊 模拟不同登录行为模式:")
    
    # 1. 正常用户（1-2次登录成功）
    for username, password in users_created[:5]:
        for _ in range(random.randint(1, 2)):
            test_login(username, password)
            time.sleep(0.1)
    
    # 2. 忘记密码用户（多次失败后成功）
    for username, password in users_created[5:8]:
        # 先尝试错误密码
        for _ in range(random.randint(3, 6)):
            test_login(username, "wrong_password")
            time.sleep(0.1)
        # 最后成功登录
        test_login(username, password)
    
    # 3. 疑似暴力破解（大量失败尝试）
    if users_created:
        target_user = users_created[0][0]
        print(f"  🔍 模拟对用户 {target_user} 的暴力破解尝试...")
        for _ in range(15):
            test_login(target_user, f"hack_attempt_{random.randint(1000, 9999)}")
            time.sleep(0.05)
    
    print("  ✅ 直方图数据生成完成")

def concurrent_load_test(duration=60, threads=10):
    """并发负载测试"""
    print(f"\n🚀 开始 {duration} 秒并发负载测试（{threads} 个线程）...")
    
    stop_event = threading.Event()
    
    def worker():
        while not stop_event.is_set():
            try:
                # 随机选择操作
                operation = random.choice(['register', 'login', 'health'])
                
                if operation == 'register':
                    username = f"load_user_{random.randint(10000, 99999)}"
                    password = f"pass_{random.randint(1000, 9999)}"
                    test_register(username, password)
                    
                elif operation == 'login':
                    username = f"user_{random.randint(1, 100)}"
                    password = "password123"
                    test_login(username, password)
                    
                elif operation == 'health':
                    test_health()
                    
                time.sleep(random.uniform(0.1, 0.5))
                
            except Exception as e:
                pass  # 忽略网络错误
    
    # 启动工作线程
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(worker) for _ in range(threads)]
        
        # 运行指定时间
        time.sleep(duration)
        stop_event.set()
        
    print("  ✅ 负载测试完成")

def monitor_metrics():
    """监控指标变化"""
    print("\n📈 监控关键指标变化...")
    
    try:
        response = test_metrics()
        if response.status_code == 200:
            lines = response.text.split('\n')
            
            # 提取关键指标
            key_metrics = [
                'login_total',
                'register_total', 
                'active_sessions_total',
                'error_total',
                'request_duration_seconds'
            ]
            
            print("  📊 当前关键指标:")
            for line in lines:
                for metric in key_metrics:
                    if line.startswith(metric) and not line.startswith('#'):
                        print(f"    {line}")
                        
    except Exception as e:
        print(f"  ❌ 获取指标失败: {e}")

def main():
    print("🎯 增强版登录监控系统测试")
    print("="*60)
    
    try:
        # 1. 健康检查
        print("\n1️⃣ 系统健康检查")
        health_response = test_health()
        if health_response.status_code == 200:
            print(f"  ✅ 系统健康: {health_response.json()}")
        else:
            print(f"  ❌ 系统异常: {health_response.status_code}")
            return
        
        # 2. 基础功能测试
        print("\n2️⃣ 基础功能测试")
        print("  📝 测试用户注册...")
        for i in range(3):
            username = f"test_user_{i}"
            password = f"password_{i}"
            response = test_register(username, password)
            print(f"    注册 {username}: {response.status_code} - {response.json()}")
        
        print("  🔐 测试用户登录...")
        response = test_login("test_user_0", "password_0")
        print(f"    登录测试: {response.status_code} - {response.json()}")
        
        # 3. 生成直方图数据
        print("\n3️⃣ 直方图数据生成")
        generate_histogram_data()
        
        # 4. 并发负载测试
        print("\n4️⃣ 并发负载测试")
        concurrent_load_test(duration=30, threads=5)
        
        # 5. 监控指标
        print("\n5️⃣ 监控指标检查")
        monitor_metrics()
        
        print("\n✅ 测试完成！")
        print("\n🔗 访问以下地址查看结果:")
        print("  • Prometheus: http://localhost:9090")
        print("  • Grafana:    http://localhost:3000 (admin/admin123)")
        print("  • Alertmanager: http://localhost:9093")
        print("\n💡 在 Grafana 中查看直方图:")
        print("  1. 打开 '登录监控系统 - 直方图分析' 仪表盘")
        print("  2. 观察响应时间、登录尝试次数、密码强度等直方图")
        print("  3. 查看告警状态和错误率趋势")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ 连接失败！请确保系统正在运行：")
        print("1. 运行 './start_system.sh' 启动完整系统")
        print("2. 或者运行 'docker-compose up -d' 启动服务")
        print("3. 等待服务完全启动后再次运行测试")

if __name__ == "__main__":
    main()