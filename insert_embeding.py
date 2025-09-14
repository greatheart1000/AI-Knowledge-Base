#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
用于连接PostgreSQL并批量插入向量数据。
确保数据库已安装并启用了pgvector扩展。
"""

import psycopg2
from psycopg2.extras import execute_batch, RealDictCursor
import sys
import os


def create_and_insert_vectors():
    """连接到PostgreSQL，创建表并批量插入向量数据。"""

    # 定义新的数据库名和表名
    new_db_name = "my_new_db"
    new_table_name = "my_new_table"

    # 数据库连接参数
    # 请根据你的实际配置修改密码
    db_params = {
        "dbname": new_db_name,
        "user": "great",
        "password": "123456",  # 替换为你的密码
        "host": "localhost",
        "port": "5432"
    }

    conn = None
    try:
        # 建立数据库连接
        # 注意: 新的数据库需要提前手动创建
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # 确保pgvector扩展已启用
        # 这一步是可选的，如果你确定已经启用，可以移除
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")

        # 定义创建表的 SQL 语句，增加一个用于存储向量的列
        sql_create_table = f"""
        CREATE TABLE IF NOT EXISTS {new_table_name} (
            id VARCHAR(255) PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            session_id VARCHAR(255),
            content TEXT,
            embedding VECTOR(3),
            timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """

        # 执行 SQL 语句来创建表
        cursor.execute(sql_create_table)
        print(f"✅ 表'{new_table_name}'创建成功或已存在。")

        # 添加 ALTER TABLE 语句来确保表有 embedding 列
        # 使用 IF NOT EXISTS 来避免重复添加列的错误
        sql_alter_table = f"""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='{new_table_name}' AND column_name='embedding') THEN
                ALTER TABLE {new_table_name} ADD COLUMN embedding VECTOR(3);
            END IF;
        END
        $$;
        """
        cursor.execute(sql_alter_table)
        conn.commit()
        print("✅ 'embedding' 列已存在或添加成功。")

        # 示例向量数据，现在包含id、内容和向量
        data_to_insert = [
            ('uuid_1', 'production_user_001', '对话1：你好，世界。', [1.0, 2.0, 3.0]),
            ('uuid_2', 'production_user_001', '对话2：如何批量处理数据？', [4.0, 5.0, 6.0]),
            ('uuid_3', 'production_user_002', '对话3：关于生产级系统的讨论。', [7.0, 8.0, 9.0])
        ]

        # 批量插入的 SQL 语句
        insert_sql = f"""
        INSERT INTO {new_table_name}
        (id, user_id, session_id, content, embedding) 
        VALUES (%s, %s, %s, %s, %s::vector)
        ON CONFLICT (id) DO NOTHING;
        """

        # 为了演示 ON CONFLICT，我们添加了一个 session_id
        # 如果 id 已存在，什么也不做，避免重复插入错误
        data_to_insert_with_session = [
            ('uuid_1', 'production_user_001', 'session_1', '对话1：你好，世界。', [1.0, 2.0, 3.0]),
            ('uuid_2', 'production_user_001', 'session_2', '对话2：如何批量处理数据？', [4.0, 5.0, 6.0]),
            ('uuid_3', 'production_user_002', 'session_3', '对话3：关于生产级系统的讨论。', [7.0, 8.0, 9.0])
        ]

        # 使用 execute_batch 高效地批量执行插入
        execute_batch(cursor, insert_sql, data_to_insert_with_session)

        # 提交事务以保存所有更改
        conn.commit()
        print(f"✅ 成功批量插入 {len(data_to_insert_with_session)} 条向量数据。")

    except psycopg2.Error as e:
        print(f"❌ 数据库操作失败: {e}")
        # 如果出错，回滚事务
        if conn:
            conn.rollback()

    finally:
        # 关闭游标和连接
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn:
            conn.close()
            print("数据库连接已关闭。")


if __name__ == "__main__":
    create_and_insert_vectors()


"""以 
 用户身份登录新的数据库：
sudo -u postgres psql -d my_new_db
 授予权限：
在 psql 终端中执行以下命令，授予 great 用户在 public schema 上创建的权限。
GRANT CREATE ON SCHEMA public TO great;
 """
