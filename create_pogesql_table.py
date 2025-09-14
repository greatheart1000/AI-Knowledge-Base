import psycopg2

def create_table_in_postgres():
    """连接PostgreSQL并创建表"""
    # 数据库连接参数
    # 确保 'password' 替换为你为 'great' 用户设置的密码
    db_params = {
        "dbname": "langgraph_memory",
        "user": "great",
        "password": "123456",  # 替换为你的密码
        "host": "localhost",
        "port": "5432"
    }

    conn = None
    try:
        # 建立数据库连接
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # 定义创建表的 SQL 语句
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS conversation_memories (
            id VARCHAR(255) PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            session_id VARCHAR(255),
            content TEXT,
            timestamp TIMESTAMP WITH TIME ZONE NOT NULL
        );
        """

        # 执行 SQL 语句
        cursor.execute(sql_create_table)
        
        # 提交事务以保存更改
        conn.commit()
        print("✅ 表'conversation_memories'创建成功或已存在。")

    except psycopg2.Error as e:
        print(f"❌ 数据库操作失败: {e}")
        # 如果出错，回滚事务
        if conn:
            conn.rollback()

    finally:
        # 关闭连接
        if conn:
            conn.close()
            print("数据库连接已关闭。")

if __name__ == "__main__":
    create_table_in_postgres()
