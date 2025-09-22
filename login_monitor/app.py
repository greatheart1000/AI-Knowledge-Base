from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, Gauge, Summary, generate_latest, Info
import time
import random
import threading
from datetime import datetime

app = Flask(__name__)

# 基础指标
login_total = Counter("login_total", "Login requests", ["status", "method"])
reg_total = Counter("register_total", "Register requests", ["status"])
latency_hist = Histogram("request_duration_seconds", "Request latency", ["method", "endpoint"])

# 新增监控指标
active_sessions = Gauge("active_sessions_total", "Number of active user sessions")
concurrent_requests = Gauge("concurrent_requests", "Number of concurrent requests")
response_size_hist = Histogram("response_size_bytes", "Response size distribution", ["endpoint"])
error_rate = Counter("error_total", "Total errors", ["error_type"])

# 业务指标
user_registrations_daily = Counter("user_registrations_daily_total", "Daily user registrations")
login_attempts_per_user = Histogram("login_attempts_per_user", "Login attempts per user", buckets=[1, 2, 3, 5, 10, 20, 50])
password_strength = Histogram("password_strength_score", "Password strength distribution", buckets=[1, 2, 3, 4, 5])

# 系统指标
app_info = Info("app_info", "Application information")
app_info.info({"version": "1.0.0", "environment": "development"})

# 响应时间摘要
request_summary = Summary("request_processing_seconds", "Request processing time", ["method"])

# 假装的数据库和会话存储
USER_DB = {}
ACTIVE_SESSIONS = set()
USER_LOGIN_ATTEMPTS = {}

def simulate_password_strength(password):
    """模拟密码强度评分"""
    score = len(password) // 2
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    return min(score, 5)

def update_active_sessions():
    """更新活跃会话数"""
    active_sessions.set(len(ACTIVE_SESSIONS))

@app.before_request
def before_request():
    """请求前置处理"""
    concurrent_requests.inc()
    request.start_time = time.time()

@app.after_request
def after_request(response):
    """请求后置处理"""
    concurrent_requests.dec()
    
    # 记录响应大小
    if hasattr(response, 'content_length') and response.content_length:
        response_size_hist.labels(endpoint=request.endpoint or 'unknown').observe(response.content_length)
    
    return response

@app.route("/login", methods=["POST"])
@request_summary.labels(method='login').time()
def login():
    start = time.time()
    
    try:
        data = request.get_json()
        if not data:
            error_rate.labels(error_type='invalid_json').inc()
            return jsonify({"status": "error", "message": "Invalid JSON"}), 400
            
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            error_rate.labels(error_type='missing_fields').inc()
            return jsonify({"status": "error", "message": "Missing fields"}), 400
        
        # 记录登录尝试
        USER_LOGIN_ATTEMPTS[username] = USER_LOGIN_ATTEMPTS.get(username, 0) + 1
        login_attempts_per_user.observe(USER_LOGIN_ATTEMPTS[username])
        
        # 模拟登录检查
        if USER_DB.get(username) == password:
            login_total.labels(status="200", method="password").inc()
            
            # 模拟会话创建
            session_id = f"{username}_{int(time.time())}"
            ACTIVE_SESSIONS.add(session_id)
            update_active_sessions()
            
            # 重置失败计数
            USER_LOGIN_ATTEMPTS[username] = 0
            
            status_code = 200
            response_data = {"status": "ok", "session_id": session_id}
        else:
            login_total.labels(status="401", method="password").inc()
            
            # 防暴力破解：太多失败尝试
            if USER_LOGIN_ATTEMPTS[username] > 5:
                error_rate.labels(error_type='too_many_attempts').inc()
                time.sleep(1)  # 模拟限流
                
            status_code = 401
            response_data = {"status": "fail", "message": "Invalid credentials"}
            
    except Exception as e:
        error_rate.labels(error_type='internal_error').inc()
        status_code = 500
        response_data = {"status": "error", "message": "Internal server error"}
    
    finally:
        # 记录请求延迟
        duration = time.time() - start
        latency_hist.labels(method="login", endpoint="/login").observe(duration)
    
    return jsonify(response_data), status_code

@app.route("/register", methods=["POST"])
@request_summary.labels(method='register').time()
def register():
    start = time.time()
    
    try:
        data = request.get_json()
        if not data:
            error_rate.labels(error_type='invalid_json').inc()
            return jsonify({"status": "error", "message": "Invalid JSON"}), 400
            
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            error_rate.labels(error_type='missing_fields').inc()
            return jsonify({"status": "error", "message": "Missing fields"}), 400
        
        if username in USER_DB:
            reg_total.labels(status="409").inc()
            status_code = 409
            response_data = {"status": "exists", "message": "User already exists"}
        else:
            # 记录密码强度
            strength = simulate_password_strength(password)
            password_strength.observe(strength)
            
            USER_DB[username] = password
            reg_total.labels(status="200").inc()
            user_registrations_daily.inc()
            
            status_code = 200
            response_data = {
                "status": "created", 
                "message": "User registered successfully",
                "password_strength": strength
            }
            
    except Exception as e:
        error_rate.labels(error_type='internal_error').inc()
        status_code = 500
        response_data = {"status": "error", "message": "Internal server error"}
    
    finally:
        # 记录请求延迟
        duration = time.time() - start
        latency_hist.labels(method="register", endpoint="/register").observe(duration)
    
    return jsonify(response_data), status_code

@app.route("/logout", methods=["POST"])
def logout():
    """退出登录接口"""
    data = request.get_json() or {}
    session_id = data.get("session_id")
    
    if session_id and session_id in ACTIVE_SESSIONS:
        ACTIVE_SESSIONS.remove(session_id)
        update_active_sessions()
        return jsonify({"status": "ok", "message": "Logged out successfully"})
    
    return jsonify({"status": "error", "message": "Invalid session"}), 400

@app.route("/health")
def health():
    """健康检查接口"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_sessions": len(ACTIVE_SESSIONS),
        "registered_users": len(USER_DB)
    })

@app.route("/metrics")
def metrics():
    """暴露 Prometheus 指标"""
    return generate_latest()

# 模拟后台任务：清理过期会话
def cleanup_sessions():
    """清理过期会话（模拟）"""
    import threading
    timer = threading.Timer(300.0, cleanup_sessions)  # 5分钟清理一次
    timer.daemon = True
    timer.start()
    
    # 模拟随机清理一些会话
    if len(ACTIVE_SESSIONS) > 0:
        sessions_to_remove = random.sample(list(ACTIVE_SESSIONS), 
                                         min(2, len(ACTIVE_SESSIONS)))
        for session in sessions_to_remove:
            ACTIVE_SESSIONS.discard(session)
        update_active_sessions()

if __name__ == "__main__":
    # 启动后台任务
    cleanup_sessions()
    
    # 初始化指标
    update_active_sessions()
    
    print("🚀 Login Monitor with Enhanced Metrics is starting...")
    print("📊 Prometheus metrics: http://localhost:5000/metrics")
    print("🛋 Health check: http://localhost:5000/health")
    
    app.run(host="0.0.0.0", port=5000, debug=True)