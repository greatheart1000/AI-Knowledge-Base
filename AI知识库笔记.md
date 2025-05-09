# AI知识库笔记

#### 公网IP 118.145.187.17

#### 私网IP 172.31.0.2

#### minIO的启动

./minio server /opt/minio/data

用户名： minioadmin

密码 ：    minioadmin

*# 后台启动（这个只能127.0.0.1访问）*

nohup ./minio server --address :9000 --console-address :9001 /opt/minio/data > /opt/minio/data/minio.log &



#### modelscope token 

3e753b42-652b-4bdd-b803-12ed41c9e449



查看mysql是否运行

sudo service mysql status

搜索"拂晓的海洋"相关资料，在浏览器不同标签打开至少5个搜索结果，将地址保存到D:\tmp，请使用中文



## git命令

```python
# 1. 确保你在 master 分支
git checkout master

# 2. 将新文件添加到暂存区
git add AI算法面试题.md

# 3. 提交更改
git commit -m "Add new file: AI算法面试题.md"

# 4. 推送到远程仓库
git push origin master

怎么用命令新建一个分支呢

git branch <new_branch_name>  (创建但不切换)

git checkout -b <new_branch_name> (创建并切换)


```

## 查看文件夹有多少个子文件夹

ls -l | grep "^d" | wc -l



```text
npx @modelcontextprotocol/inspector -e YML= /root/llm_AI/config.yml /root/miniconda3/envs/mcp/bin/python -m xiyan_mcp_server
```

#### mysql 启动命令

sudo service mysql start

python 连接mysql  

```python
import pymysql

# 数据库连接配置
db_config = {
    'host': 'localhost',          # 数据库主机地址
    'user': 'root',               # 数据库用户名
    'password': 'Greatheart123%',         # 数据库密码
    'database': 'my_database',    # 连接的数据库名称
    'charset': 'utf8mb4'          # 字符集
}
# 创建数据库连接
connection = pymysql.connect(**db_config)

try:
    with connection.cursor() as cursor:
        # 执行查询示例
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print("Database version:", version)

finally:
    # 关闭连接
    connection.close()

```

#### 服务地址

http://118.145.187.17

http://118.145.187.17/large

#### 算法服务启动命令

nohup python llm_argm.py > app.log 2>&1 &









#### neo4j知识图谱启动命令

```bash
启动命令 neo4j console

控制面板  


```

#### Pinecone向量数据库

API key：  pcsk_6poB8p_3mJ5SqmcHczjmva8AveuFyX1jgvXxFy29QScQLTgbLiK63An49WktRE4sHoc9Ut





#### 向量数据库

```
运行Weaviate容器

docker run -d --name weaviate \
    --restart=always \
    -p 8088:8088 \
    -p 50051:50051 \
    -e "AUTHENTICATION_APIKEY_ENABLED=true" \
    -e "AUTHENTICATION_APIKEY_ALLOWED_KEYS=test-secret-key,test2-secret-key" \
    -e "AUTHENTICATION_APIKEY_USERS=greatheart1000@163.com,1352744183@qq.com" \
    -e "AUTHORIZATION_ADMINLIST_ENABLED=true" \
    -e "AUTHORIZATION_ADMINLIST_USERS=greatheart1000@163.com" \
    -e "AUTHORIZATION_ADMINLIST_READONLY_USERS=1352744183@qq.com" \
    -e WEAVIATE_HOSTNAME=0.0.0.0 \
    semitechnologies/weaviate:latest

```



##### 向量数据库插入数据

```python
from pinecone.grpc import PineconeGRPC as Pinecone

pc = Pinecone(api_key="pcsk_6poB8p_3mJ5SqmcHczjmva8AveuFyX1jgvXxFy29QScQLTgbLiK63An49WktRE4sHoc9Ut")

# To get the unique host for an index, 
# see https://docs.pinecone.io/guides/data/target-an-index
index = pc.Index(host="INDEX_HOST")

upsert_response = index.upsert(
  vectors=[
    {'id': 'vec1',
      'values': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
      'sparse_values': {
          'indices': [1, 5],
          'values': [0.5, 0.5]
      }},
    {'id': 'vec2',
      'values': [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
      'sparse_values': {
          'indices': [5, 6],
          'values': [0.4, 0.5]
      }}
  ],
  namespace='example-namespace'
)

```

##### Pinecone 将文本语料库转换为稀疏向量

```python

```



##### milvus 编译安装

[源码编译部署篇（一）成功安装Milvus!零基础Ubuntu部署安装Milvus教程_ubuntu安装milvus-CSDN博客](https://blog.csdn.net/qq_43893755/article/details/135339396)

```python
111111111111
```



#### 新增标签

```bash
curl -i -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: HMAC-SHA256***' \
  https://api-vikingdb.volces.com/api/collection/create \
  -d '{
    "collection_name": "my_knowledge_base",
    "description": "我的测试知识库",  
    "fields": [                             
        {
            "field_name": "行业标签",     
            "field_type": "list<string>",
             "default_val": ["IT和软件" ,"金融服务","医疗保健","教育"]
        },
        {
            "field_name": "主题标签",                   
            "field_type": "list<string>",
            "default_val": ["物联网" ,"网络安全","云计算","数据分析"]
        },
        {
            "field_name": "文档类型",
            "field_type": "list<string>", 
            "default_val": ["报告" ,"论文","文章"]
        }
        ]  
}'
```





#### 创建知识库接口

非结构化数据

文件的主要内容为文本和图表，如文章、报告、书籍等，支持 faq.xlsx、docx、pptx、pdf、markdown、txt 格式

结构化数据  

文件的主要内容为结构化文本，需具备明确的字段约束，如问答总结、政策条款、数据收集等，支持 csv、xlsx、jsonl、faq.xlsx 格式

```bash

data_type=1  创建非结构化数据

curl -X POST http://127.0.0.1:5000/create_collection -H "Content-Type: application/json" -d '{"name": "my_knowledgeBase", "description": "我的测试用例", "data_type": 1,"length":"2000"}'

curl -X POST http://127.0.0.1:5000/create_collection \
-H "Content-Type: application/json" \
-d '{
  "name": "my_knowledgeBase",
  "description": "我的测试用例",
  "data_type": 1,
  "length": "2000",
  "tags": {
    "category": "计算机",
    "importance": "一般",
    "visibility": "yes"
  }
}'
新的

curl -X POST http://127.0.0.1:5000/create_collection \
-H "Content-Type: application/json" \
-d '{
  "name": "my_knowledgeBase",
  "description": "我的测试用例",
  "data_type": 1,
  "length": 2000,
  "tags": [
    {"name": "category", "type": "string", "value": "计算机"},
    {"name": "importance", "type": "string", "value": "一般"},
    {"name": "visibility", "type": "bool", "value": true},
    {"name": "size", "type": "int", "value": 1024}
  ]
}'



data_type=0  创建结构化数据    

curl -X POST http://127.0.0.1:5000/create_collection -H "Content-Type: application/json" -d '{"name": "stru_knowledgeBase", "description": "结构化数据测试用例", "data_type":0,"length":"2000"}'

```

```bash
 {'vector_field':
 		{'field_name': '_sys_auto_content_vector', 'field_type': 'vector', 'dim': 2048}, 			  	    		'sparse_vector_field': 
 				{'field_name': '_sys_auto_content_sparse_vector', 
 				'field_type': 'sparse_vector'}, 	
 		'cpu_quota': 1, 
 		'distance': 'ip', 
 		'quant': 'int8', 
 		'embedding_model': 'doubao-embedding-and-m3', 
 		'embedding_dimension': 2048,
        'need_instruction': True, 
        'fields': [
        			{'field_name': '_sys_auto_id', 'field_type': 'string'}, 
        			{'field_name': '_sys_auto_doc_id', 'field_type': 'string'}, 
        			{'field_name': '_sys_auto_chunk_id', 'field_type': 'int64'}, 
        			{'field_name': '_sys_auto_doc_type', 'field_type': 'string'}, 
        			{'field_name': '_sys_auto_add_type', 'field_type': 'string'},
                    {'field_name': '_sys_auto_sub_index', 'field_type': 'string', 'default_val': 'default'}, 					 {'field_name': '行业', 'field_type': 'list<string>'},
                    {'field_name': '重要性', 'field_type': 'list<string>'},
                    {'field_name': '是否公开', 'field_type': 'bool'}, 
                    {'field_name': 'doc_id', 'field_type': 'string'}, 
                    {'field_name': 'doc_name', 'field_type': 'string'}
                    ], 
          'field_enumerated_list': '{"行业":["金融","计算机","IT"],
           							"重要性":["非常","一般","不重要"]}', 
          'has_sparse_vector': True, 
          'title_entity_extraction': False, 
          'embedding_model_version': '240715'}
          
      
      
     [{'field_name': '_sys_auto_id', 'field_type': 'string'}, 
     {'field_name': '_sys_auto_doc_id', 'field_type': 'string'}, 
     {'field_name': '_sys_auto_chunk_id', 'field_type': 'int64'}, 
     {'field_name': '_sys_auto_doc_type', 'field_type': 'string'},
     {'field_name': '_sys_auto_add_type', 'field_type': 'string'}, 
     {'field_name': '_sys_auto_sub_index', 'field_type': 'string', default_val': 'default'}, 
     {'field_name': '行业', 'field_type': 'list<string>'}, 
     {'field_name': '是否公开', 'field_type': 'bool'}, 
     {'field_name': '重要性', 'field_type': 'list<string>'}], 
     'has_sparse_vector': True, 
     'title_entity_extraction': False, 
     'embedding_model_version': '240715'}
```





#### 向已创建知识库导入文档

add_doc

doc_id   **知识库下的文档唯一标识**

- 只能使用英文字母、数字、下划线_，并以英文字母开头，不能为空

- 长度要求：[1, 128]‘

- 多次上传，重复的 doc_id 会进行覆盖（新上传的覆盖旧的）

- "add_type" == "url" 时，该字段必传

- "add_type" == "tos" 时，该字段无效，系统会自动从 tos 文件的 meta 中获取[知识库常见问题](https://www.volcengine.com/docs/84313/1324074)

上传非结构化数据资料 

```bash

curl -X POST http://localhost:5000/add_doc \
     -H "Content-Type: application/json" \
     --no-buffer \
     -d '{"name": "unstructure_Data",
     "doc_id": "m12345",
     "doc_name": "个人简历",
     "doc_type": "pdf",
     "url": "http://118.145.187.17:42723/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL2NhaWppYW4vJUU2JUIxJTg5JUU1JTg1JThCJUU2JTk3JUI2JUU0JUJCJUEzLSVFNSVBNCVBNyVFNiU5NSVCMCVFNiU4RCVBRSVFNiU4QyU5NiVFNiU4RSU5OC0lRTclOUYlQjMlRTYlOTYlODclRTUlOTAlOUIucGRmP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9R0g2SUVFRE85R0dVUENSVkhPSUslMkYyMDI0MTIxOCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNDEyMThUMDMyMDE3WiZYLUFtei1FeHBpcmVzPTQzMjAwJlgtQW16LVNlY3VyaXR5LVRva2VuPWV5SmhiR2NpT2lKSVV6VXhNaUlzSW5SNWNDSTZJa3BYVkNKOS5leUpoWTJObGMzTkxaWGtpT2lKSFNEWkpSVVZFVHpsSFIxVlFRMUpXU0U5SlN5SXNJbVY0Y0NJNk1UY3pORFV6TlRFNU9Td2ljR0Z5Wlc1MElqb2liV2x1YVc5aFpHMXBiaUo5Lm1rRFM0c1V3NXQ5S1NtanNaTWRVMHRobDB3ck5fQVdvb19oYTR0MldzbkJtZHlublpwY2ZKbGtwSno1NnJ3aDFOU2FMWXRSLU40cHJadTcxWnhFaWlnJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZ2ZXJzaW9uSWQ9bnVsbCZYLUFtei1TaWduYXR1cmU9M2IyZDVjZWZhYzRhNzQzYzZlYmQ5Zjk1ZTI5YjNiMDU4ZDAyYTY3NmM0YjBkZjE0YjVlYTc5NzEzY2RkMWM0ZA",
     "meta":[
                {"field_name":"行业","field_type":"string", "field_value":"企业服务"},
                {"field_name":"是否公开","field_type":"bool", "field_value":true}
    ]}'
    
 
```



```bash
curl -X POST http://localhost:6000/add_doc \
     -H "Content-Type: application/json" \
     --no-buffer \
     -d '{"name": "test_0006",
     "doc_id": "m1234567",
     "doc_name": "行业",
     "doc_type": "pptx",
     "url": "http://118.145.187.17:9001/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL2NhaWppYW4vNGZiYWU4M2YtZjExMS00YWE1LWJlMjctODIxMWE2MzRiODA0LSVFOCVBMSU4QyVFNCVCOCU5QSVFNiU5NiVCMHBwdC5wcHR4P1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9T1pEQ0lNRzZYMkZOUkRBUzhJWVQlMkYyMDI1MDEwMyUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNTAxMDNUMDM0ODI1WiZYLUFtei1FeHBpcmVzPTQzMjAwJlgtQW16LVNlY3VyaXR5LVRva2VuPWV5SmhiR2NpT2lKSVV6VXhNaUlzSW5SNWNDSTZJa3BYVkNKOS5leUpoWTJObGMzTkxaWGtpT2lKUFdrUkRTVTFITmxneVJrNVNSRUZUT0VsWlZDSXNJbVY0Y0NJNk1UY3pOVGt4T1RFM05Dd2ljR0Z5Wlc1MElqb2liV2x1YVc5aFpHMXBiaUo5LnBtOHIzSU92bUZTSDBlWlAzLXNqc1k0MGlMX1JXa29SSGJXbGJtNzhZbkZwZTNsUEtBMHJyU2gwYnYxZE1TTmhLakVMWC1TdnhwTEdsVU9aT2Vhc2hRJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZ2ZXJzaW9uSWQ9bnVsbCZYLUFtei1TaWduYXR1cmU9YjEyOGQ5M2EyOTRkZWQzN2UwZDY5YzZkZmYzMzI2NmNiYTMzOWE4MjA1YmVkMzE0MTYyYTk2NjA1ZTUzNTViNw",
     "meta":[
                {"field_name":"行业","field_type":"string", "field_value":"企业服务"},
                {"field_name":"是否公开","field_type":"bool", "field_value":true}
    ],
    "dedup":{"content_dedup":true,
              "doc_name_dedup":true,
              "auto_skip":true }

    }'
```





上传结构化数据资料 

```bash
http://118.145.187.17:42927/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL2NhaWppYW4vdGVzdF9RQS54bHN4P1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9WExTQkM1N1A1WFBGU1BNRFpMUFQlMkYyMDI0MTIyMCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNDEyMjBUMDg0NDA0WiZYLUFtei1FeHBpcmVzPTQzMTk5JlgtQW16LVNlY3VyaXR5LVRva2VuPWV5SmhiR2NpT2lKSVV6VXhNaUlzSW5SNWNDSTZJa3BYVkNKOS5leUpoWTJObGMzTkxaWGtpT2lKWVRGTkNRelUzVURWWVVFWlRVRTFFV2t4UVZDSXNJbVY0Y0NJNk1UY3pORGN5TnpNMk5Dd2ljR0Z5Wlc1MElqb2liV2x1YVc5aFpHMXBiaUo5Ll9RWi0xRGhvYWNCVkxDUFByeUVtOFdiQmU5Ty10NTE2Zm55NFNPREtrRXcydFlPWC02Y3FTQmEyTmZSTTlESEpPT2J4NExtRV93VUZadzRzUUtxbmt3JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZ2ZXJzaW9uSWQ9bnVsbCZYLUFtei1TaWduYXR1cmU9YzhjODQ0ODE4YmIxMzU1NTc4NDZjZjI5Y2UyYzA1Mjg4M2QxZWJkMDM4OWE3MDI5OTI1YmNmMjNhNTdjNmIwOA
# csv ,jsonl, xlsx,

curl -X POST http://localhost:6000/add_doc \
     -H "Content-Type: application/json" \
     --no-buffer \
     -d '{"name": "stru_knowledgeBase",
     "doc_id": "mtest_csv111",
     "doc_name": "问答数据集csv111",
     "doc_type": "csv",
     "url": "http://118.145.187.17:42927/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL2NhaWppYW4vb3V0cHV0LmNzdj9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPVhMU0JDNTdQNVhQRlNQTURaTFBUJTJGMjAyNDEyMjAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMjIwVDA5MTEyOFomWC1BbXotRXhwaXJlcz00MzIwMCZYLUFtei1TZWN1cml0eS1Ub2tlbj1leUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaFkyTmxjM05MWlhraU9pSllURk5DUXpVM1VEVllVRVpUVUUxRVdreFFWQ0lzSW1WNGNDSTZNVGN6TkRjeU56TTJOQ3dpY0dGeVpXNTBJam9pYldsdWFXOWhaRzFwYmlKOS5fUVotMURob2FjQlZMQ1BQcnlFbThXYkJlOU8tdDUxNmZueTRTT0RLa0V3MnRZT1gtNmNxU0JhMk5mUk05REhKT09ieDRMbUVfd1VGWnc0c1FLcW5rdyZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmdmVyc2lvbklkPW51bGwmWC1BbXotU2lnbmF0dXJlPWNlYThkMTkzNDM1NGM1ZjU0NmMyZWZkYzNhOTZhNTE0OGFiMGM3YmYwZTI2ODRkYzBiM2IwY2Y4OTg4ZDhmNTQ",
     "meta":[
                {"field_name":"行业","field_type":"string", "field_value":"招聘数据"},
                {"field_name":"是否公开","field_type":"bool", "field_value":true}
    ]}'
    
  
 curl -X POST http://localhost:6000/add_doc \
     -H "Content-Type: application/json" \
     --no-buffer \
     -d '{"name": "stru_knowledgeBase",
     "doc_id": "jsonl_data",
     "doc_name": "jsonl问答数据集",
     "doc_type": "jsonl",
     "url": "http://118.145.187.17:42927/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL2NhaWppYW4vb3V0cHV0Lmpzb25sP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9WExTQkM1N1A1WFBGU1BNRFpMUFQlMkYyMDI0MTIyMCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNDEyMjBUMDk1NDM1WiZYLUFtei1FeHBpcmVzPTQzMjAwJlgtQW16LVNlY3VyaXR5LVRva2VuPWV5SmhiR2NpT2lKSVV6VXhNaUlzSW5SNWNDSTZJa3BYVkNKOS5leUpoWTJObGMzTkxaWGtpT2lKWVRGTkNRelUzVURWWVVFWlRVRTFFV2t4UVZDSXNJbVY0Y0NJNk1UY3pORGN5TnpNMk5Dd2ljR0Z5Wlc1MElqb2liV2x1YVc5aFpHMXBiaUo5Ll9RWi0xRGhvYWNCVkxDUFByeUVtOFdiQmU5Ty10NTE2Zm55NFNPREtrRXcydFlPWC02Y3FTQmEyTmZSTTlESEpPT2J4NExtRV93VUZadzRzUUtxbmt3JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZ2ZXJzaW9uSWQ9bnVsbCZYLUFtei1TaWduYXR1cmU9MTlkMmY4OWQ2NTJiNGFiODMzMjExZWE2ZjA1NjNlN2I3MWEwNDdkNzRlNzU2YTAyMjExNTI3ZDMyZDViNzVjMQ",
     "meta":[
                {"field_name":"行业","field_type":"string", "field_value":"招聘数据"},
                {"field_name":"是否公开","field_type":"bool", "field_value":true}
    ]}' 
  
  

```









#### 查询知识库接口

collection_info

```bash
curl -X POST http://127.0.0.1:5000/collection_info -H "Content-Type: application/json" -d '{"name": "twst"}'

curl -X POST http://127.0.0.1:5000/collection_info -H "Content-Type: application/json" -d '{"name": "woyuyu"}'
```



#### 查看列出所有的知识库

list_collections

```bash
curl -X POST http://127.0.0.1:5000/list_collections -H "Content-Type: application/json"


list_collections  success,[{'collection_name': 'test_collection20', 'description': '我的测试用例', 'project': 'default', 'create_time': '2024-12-19 10:32:22', 'doc_num': None}, {'collection_name': 'unStructured', 'description': '这是一个非结构性文档集合', 'project': 'default', 'create_time': '2024-12-18 16:52:22', 'doc_num': None}, {'collection_name': 'unStructured111', 'description': '这是一个非结构性文档集合', 'project': 'default', 'create_time': '2024-12-18 16:34:46', 'doc_num': 1}, {'collection_name': 'woyuyu', 'description': '更新知识库的描述', 'project': 'default', 'create_time': '2024-12-17 17:36:30', 'doc_num': None}, {'collection_name': 'twst', 'description': '测试', 'project': 'default', 'create_time': '2024-12-17 10:42:44', 'doc_num': 2}, {'collection_name': 'first_use', 'description': '第一次使用', 'project': 'default', 'create_time': '2024-12-12 09:29:06', 'doc_num': 1}, {'collection_name': 'haihao', 'description': '好', 'project': 'default', 'create_time': '2024-12-10 15:57:37', 'doc_num': 2}, {'collection_name': 'shoudong_', 'description': '测试知识库', 'project': 'default', 'create_time': '2024-12-10 11:53:31', 'doc_num': 1}, {'collection_name': 'MyNewCollection', 'description': 'This is a new collection for structured data.', 'project': 'default', 'create_time': '2024-11-18 02:17:27', 'doc_num': 1}, {'collection_name': 'unstructure_Data', 'description': '这是一个非结构性文档集合', 'project': 'default', 'create_time': '2024-11-08 06:58:29', 'doc_num': 1}, {'collection_name': 'ppt111', 'description': '这是一个ppt非结构性文档', 'project': 'default', 'create_time': '2024-11-06 01:49:10', 'doc_num': 4}, {'collection_name': 'zhaopin', 'description': 'New description for the collection', 'project': 'default', 'create_time': '2024-11-05 07:40:22', 'doc_num': 1}]

```





#### 更新知识库的描述接口  

update_collection

```bash
curl -X POST http://127.0.0.1:5000/update_collection -H "Content-Type: application/json" -d '{"name": "woyuyu","description": "更新知识库的描述"}'

{
  "result": "update_collection success"
}

@app.route('/update_collection', methods=['POST'])
def update_collection():
    try:
        logger.info(f"===== update_collection用于更新已有的指定知识库Collection配置 =====")
        data = request.get_json()  # 从POST请求中获取数据
        name =data['name']
        description =data['description']
        my_collection = viking_knowledgebase_service.update_collection(name, description=description, cpu_quota=1)
        print(my_collection)
        result = {"result":"update_collection success",'status_code': 200}
        logger.info(f"{result}")
        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({'message': 'update_collection  failed', 'status_code': 300})

```



#### 查看知识库下某个文档信息 

get_doc

```bash
参考接口 https://www.volcengine.com/docs/82379/1273568

curl -X POST http://127.0.0.1:5000/get_doc -H "Content-Type: application/json" -d '{"name": "unstructure_Data","doc_id": "pdf_zhaopin"}'

```

#### 查询某个知识库下所有文档信息

list_docs

按照更新时间从最近到最远排序

```bash
curl -X POST http://127.0.0.1:5000/list_docs -H "Content-Type: application/json" -d '{"name": "struced_csv"}'

结果如下:
[{'doc_name': 'oo', 'doc_id': 'a93dbf5b1e7c14a11966d02b0d210fe15', 'doc_type': 'csv', 'create_time': '2024-12-30 20:17:57', 'update_time': '2024-12-30 20:18:01', 'process_status': 1}, {'doc_name': '行业新6', 'doc_id': 'ae4c3854c0e484fca90c0678959aa12cf', 'doc_type': 'csv', 'create_time': '2024-12-30 20:16:56', 'update_time': '2024-12-30 20:16:59', 'process_status': 1}, {'doc_name': 'output', 'doc_id': 'acd4370dec48f4ea58197526ba02cf7fc', 'doc_type': 'csv', 'create_time': '2024-12-30 20:15:06', 'update_time': '2024-12-30 20:15:26', 'process_status': 0}, {'doc_name': '行业新6', 'doc_id': 'a400effafed104ee492636c5b1c95bef4', 'doc_type': 'csv', 'create_time': '2024-12-30 20:12:34', 'update_time': '2024-12-30 20:12:38', 'process_status': 1}, {'doc_name': '行业新1', 'doc_id': 'a8d301c2cccb84eea820f0ec829c3f6ed', 'doc_type': 'csv', 'create_time': '2024-12-30 20:08:19', 'update_time': '2024-12-30 20:08:22', 'process_status': 1}, {'doc_name': '行业新1', 'doc_id': 'ad49e2bb3b964405a9dd829bd3dfed69e', 'doc_type': 'csv', 'create_time': '2024-12-30 20:05:37', 'update_time': '2024-12-30 20:05:41', 'process_status': 1}]
process_status: 0为处理成功 ， process_status：1 为处理失败
```



#### 查看某个知识库下知识点信息

list_points

查看某个知识库下的知识点信息 默认按照point_id从小到大排序

[list_points--火山方舟大模型服务平台-火山引擎](https://www.volcengine.com/docs/82379/1273573)

```bash
curl -X POST http://127.0.0.1:5000/list_points -H "Content-Type: application/json" -d '{"name": "unstructure_Data"}'

curl -X POST http://127.0.0.1:5000/list_points -H "Content-Type: application/json" -d '{"name": "ppt111"}'

curl -X POST http://127.0.0.1:5000/list_points -H "Content-Type: application/json" -d '{"name": "CCSS2213"}'
```



#### 查看某知识库下所有知识点信息(新)

fetch_point

```bash
查询结构化知识库
curl -X POST http://127.0.0.1:5000/fetch_point -H "Content-Type: application/json" -d '{"name": "struced_csv"}'

查询非结构化知识库
curl -X POST http://127.0.0.1:5000/fetch_point -H "Content-Type: application/json" -d '{"name": "y"}'

```







#### 从知识库删除文档

delete_doc

 **name: 知识库名  doc_id : 该知识库下所要删除的文档**



```bash
curl -X POST http://127.0.0.1:5000/delete_doc -H "Content-Type: application/json" -d '{"name": "unstructure_Data","doc_id":"m12345"}'

{
  "message": " delete m12345 from collection unstructure_Data success ",
  "status_code": 200,
  "timestamp": "2024-12-18 14:58:10"
}

```

#### 增加切片信息接口

point_add 接口用于新增一个知识库下某个文档的一个切片

name：**知识库名称**

doc_id: **表示新增切片所属的文档**

chunk_type: **要添加的切片类型**

- 结构化知识库：“structured”，
- 非结构化知识库：
  - “text”： 纯文本切片
  - “faq”： faq类型切片

content:  **新增切片文本内容**

- chunk_type 为 text/faq 时必传。
- chunk_type 为 text 时，表示要添加的非结构化文档的切片内容。chunk_type 为 faq 时，表示答案字段。

question  chunk_type 为 faq 时必传

```bash
curl -X POST http://127.0.0.1:5000/delete_point \
     -H "Content-Type: application/json" \
     -d '{"name": "collection22",
          "point_id": "a735fcab3c539436cadfa2743a793d563-100"
          }'

doc_id     表示新增切片所属的文档doc_id 表示新增切片所属的文档 
chunk_type 表示要添加的切片类型
非结构化数据 第一种情况 text 
curl -X POST http://127.0.0.1:5000/point_add \
     -H "Content-Type: application/json" \
     -d '{"name": "collection22",
     	  "collection_type":1,
          "doc_id": "ad68d3cd235d24ec0854e9457285a0607",
          "chunk_type": "text",
          "content":"要添加的切片类型11111" 
          }'
 
非结构化数据 第二种情况 faq
curl -X POST http://127.0.0.1:5000/point_add \
     -H "Content-Type: application/json" \
     -d '{"name": "collection22",
     	  "collection_type":1,
          "doc_id": "ad68d3cd235d24ec0854e9457285a0607",
          "chunk_type": "faq",
          "question":"你是谁?11111",
          "content":"要添加的切片类型11111" 
          }'
  
{'code': 0, 'data': {'collection_name': 'collection22', 'project': 'default', 'resource_id': 'kb-e190efb3dec08c49', 'doc_id': 'ad68d3cd235d24ec0854e9457285a0607', 'chunk_id': 127, 'point_id': 'ad68d3cd235d24ec0854e9457285a0607-127'}, 'message': 'success', 'request_id': '02173494016423400000000000000000000ffff0a00787240d69b'}


第三种情况 结构化知识库：“structured”
fields字段与知识库的字段保持一致 
curl -X POST http://127.0.0.1:5000/point_add \
     -H "Content-Type: application/json" \
     -d '{"name": "stru_knowledgeBase",
          "collection_type":0,
          "doc_id": "mtest_csv111",
          "chunk_type": "structured",
          "fields":[
                {"field_name": "问题" ,"field_value": "你是谁啊" },
                {"field_name": "答案" ,"field_value": "你是谁啊" },
            ]
          }'
{'code': 0, 'data': {'collection_name': 'stru_knowledgeBase', 'project': 'default', 'resource_id': 'kb-f8d375e1957f5b4d', 'doc_id': 'mtest_csv111', 'chunk_id': 114, 'point_id': 'mtest_csv111-114'}, 'message': 'success', 'request_id': '02173493915706200000000000000000000ffff0a007c33b8cc3c'}



a11_11

curl -X POST http://127.0.0.1:5000/point_add \
     -H "Content-Type: application/json" \
     -d '{
           "name": "a11_11",
           "collection_type": 0,
           "doc_id": "aefc05c8310264e8da79663289cbbbc88",
           "chunk_type": "structured",
           "fields": [
             {"field_name": "问题", "field_value": "你是谁啊"},
             {"field_name": "答案", "field_value": "你是谁啊"}
           ]
         }'
```





#### 删除切片接口

delete_point 从知识库删除一个知识库下的某个切片 

name：**知识库名称**

point_id：要删除的切片id

```bash
curl -X POST http://127.0.0.1:5000/delete_point \
     -H "Content-Type: application/json" \
     -d '{"name": "collection22",
          "point_id": "a735fcab3c539436cadfa2743a793d563-100"
          }'

{"code":0,"message":"success","request_id":"02173493753806200000000000000000000ffff0a00640fd2f016"}

curl -X POST http://127.0.0.1:5000/delete_point \
     -H "Content-Type: application/json" \
     -d '{"name": "collection22",
          "point_id": "a735fcab3c539436cadfa2743a793d563-98"
          }'
          
curl -X POST http://127.0.0.1:5000/delete_point \
     -H "Content-Type: application/json" \
     -d '{"name": "cdd123",
          "point_id": "a735fcab3c539436cadfa2743a793d563-98"
          }'
   先查询
curl -X POST http://127.0.0.1:5000/list_points -H "Content-Type: application/json" -d '{"name": "CCSS2213"}'      
          
CCSS2213  point_id  a4d487847f16642fc8373eb33db8a7ac3-88
curl -X POST http://127.0.0.1:5000/delete_point \
     -H "Content-Type: application/json" \
     -d '{"name": "CCss2213",
          "point_id": "a4d487847f16642fc8373eb33db8a7ac3-10"
          }'

```



#### 更新知识库下的切片内容

更新知识库下切片内容，目前可以更新非结构化切片的content字段和结构化切片的fields字段

point_id：**要更新的切片 id**

content：**要更新的非结构化文档的切片内容**

fields：要更新的结构化文档的切片内容，一行数据全量更新
[
{ "field_name": "xxx" // 字段名称
"field_value": xxxx // 字段值
},
]
字段名称必须已在collection里配置，否则会报错。

question：**要更新的非结构化faq文档切片的问题字段**

collection_type 非结构化数据 为 1   结构化数据  collection_type 0

```bash
更新的非结构化数据切片内容  text
curl -X POST http://127.0.0.1:5000/point_update \
     -H "Content-Type: application/json" \
     -d '{"name": "collection22",
     	 "collection_type":1,
          "point_id": "a735fcab3c539436cadfa2743a793d563-98",
          "content":"好的"}'
          
{"code":0,"message":"success","request_id":"02173494384970800000000000000000000ffff0a004c353f1a8a"}

更新非结构化数据切片内容 faq

curl -X POST http://127.0.0.1:5000/point_update \
     -H "Content-Type: application/json" \
     -d '{"name": "collection22",
     	  "collection_type":1,
          "point_id":"ad68d3cd235d24ec0854e9457285a0607-5",
          "question":"你是谁?11111",
    	  "content":"要添加的切片类型11111" }'
          
{"code":0,"message":"success","request_id":"02173494384970800000000000000000000ffff0a004c353f1a8a"}



更新结构化数据切片内容 
curl -X POST http://127.0.0.1:5000/point_update \
     -H "Content-Type: application/json" \
     -d '{"name": "stru_knowledgeBase",
     	 "collection_type":0,
          "point_id": "mtest_csv111-20",
          "fields":[
                {"field_name": "问题" ,"field_value": "你是谁啊" },
                {"field_name": "答案" ,"field_value": "你是谁啊" },
            ]
}'
          
{"code":0,"message":"success","request_id":"02173494384970800000000000000000000ffff0a004c353f1a8a"}

```



#### 查看知识库下指定切片信息

[info--向量数据库VikingDB-火山引擎](https://www.volcengine.com/docs/84313/1386606)

point_info

```bash
curl -X POST http://127.0.0.1:5000/point_info \
     -H "Content-Type: application/json" \
     -d '{"name": "unStructured111",
          "query": "候选人的个人信息是什么"
          }'
```



#### 更新文档信息

update_meta

```bash
curl -X POST http://127.0.0.1:5000/update_meta \
     -H "Content-Type: application/json" \
     -d '{"name": "unstructure_Data",
          "doc_id": "pdf_zhaopin",
          "meta": [
              {"field_name": "行业", "field_type": "string", "field_value": "企业服务"},
              {"field_name": "是否公开", "field_type": "bool", "field_value": true}
          ]}'
          
{
  "message": "update meta pdf_zhaopin from collection unstructure_Data success ",
  "status_code": 200,
  "timestamp": "2024-12-18 15:18:23"
}

```



#### 对知识库进行检索重排大模型回答（new）

对知识库进行检索和前后处理 

search_knowledge

```bash
curl -X POST http://127.0.0.1:6000/search_knowledge      -H "Content-Type: application/json"      -d '{"name": "test_00099",
          "query": "请你介绍一下软通动力信息技术"
          }'

          
{'query': '请你介绍一下软通动力旗下布局3大智能制造工厂分别在哪里', 'answer': '软通动力旗下布局的 3 大智能制造工厂分别位于北京、深圳和南京。', 'relation_knowledges': {'query': '请你介绍一下软通动力旗下布局3大智能制造工厂分别在哪里', 'rewrite_query': '软通动力旗下布局的3大智能制造工厂分别位于哪些地方？', 'rerank_result': [{'content': '北京\n深圳\n南京\n杭州\n9\n[©2024本文档版权归软通动力信息技术（集团）股份有限公司所有，并保留所有权利。\n布局3大智能制造工厂，通过利用 人工智能与柔性自动化技术，打 造全球先进的“灯塔工厂”]iSOFTSTONE 软通动力', 'score': '0.9917', 'title': '布局全球业务和智能制造工厂©2024本文档版权归软通动力信息技术（集团）股份有限公司所有，并保留所有权利。\n布局3大智能制造工厂，通过利用 人工智能与柔性自动化技术，打 造全球先进的“灯塔工厂”'}, {'content': '[布局3大智能制造工厂，通过利用 人工智能与柔性自动化技术，打 造全球先进的“灯塔工厂”\n武汉]iSOFTSTONE 北京 江苏苏州工厂 城市副中心工厂', 'score': '0.9897', 'title': '布局3大智能制造工厂，通过利用 人工智能与柔性自动化技术，打 造全球先进的“灯塔工厂”\n武汉'}, {'content': '北京\n[深圳\n布局3大智能制造工厂,通过利 用人工智能与柔性自动化技术, 打造全球先进的"灯塔工厂"]iSOFTSTONE 软通动力', 'score': '0.9889', 'title': '布局全球业务和智能制造工厂深圳\n布局3大智能制造工厂,通过利 用人工智能与柔性自动化技术, 打造全球先进的"灯塔工厂"'}, {'content': '[布局3大智能制造工厂,通过利 用人工智能与柔性自动化技术, 打造全球先进的"灯塔工厂"\n武汉]iSOFTSTONE 北京 江苏苏州工厂 城市副中心工厂', 'score': '0.9887', 'title': '布局3大智能制造工厂,通过利 用人工智能与柔性自动化技术, 打造全球先进的"灯塔工厂"\n武汉'}, {'content': '[布局3大智能制造工厂，通过利用 人工智能与柔性自动化技术，打 造全球先进的“灯塔工厂”\n武汉]江苏无锡工厂', 'score': '0.9810', 'title': '布局3大智能制造工厂，通过利用 人工智能与柔性自动化技术，打 造全球先进的“灯塔工厂”\n武汉'}]}, 'cost_time': 3.004, 'status_code': 200}

```



#### 向大模型发起对话请求

基于多轮历史对话，使用大语言模型进行回答生成

```bash
curl -X POST http://127.0.0.1:6000/chat_llm \
     -H "Content-Type: application/json" \
     -d '{"query": "给我讲氧化铝的用途"}'
     
 result: {'query': '给我讲氧化铝的用途', 'answer': '嘿，同学们！今天咱们来聊聊氧化铝的用途。氧化铝可是个厉害的家伙哦！\n\n首先呢，它可以用来制造各种陶瓷制品，比如那些漂亮的瓷器，就是因为有了氧化铝才变得坚固又耐用。\n\n然后呢，氧化铝还能在电子领域大展身手，它是制造集成电路板的重要材料哦！\n\n还有哦，它在航空航天领域也有一席之地，可以用来制造耐高温的部件。\n\n另外，氧化铝还可以作为催化剂，帮助化学反应更快地进行。\n\n总之，氧化铝的用途非常广泛，就像一个多才多艺的小能手！同学们，你们记住了吗？'}
```



#### 对知识片段进行重排序

knowledge_rerank

```bash
curl -X POST http://127.0.0.1:6000/knowledge_rerank \
     -H "Content-Type: application/json" \
     -d '{"datas": [
     
     {
        "query": "退改",
        "content": "如果您需要人工服务，可以拨打人工客服电话：4006660921",
        "title":"无"
    }, 
    
    {
        "query": "退改",
        "content": "1、1日票 1.5日票 2日票的退款政策： -到访日前2天的00:00前，免费退款 - 到访日前2天的00:00至到访日前夜23:59期间,退款需扣除服务费（人民币80元） - 到访日当天（00:00 之后），不可退款 2、半日票的退款政策： - 未使用的门票可在所选入...",
        "title":"门票退改政策｜北京环球影城的门票退改政策"
    }, 
    
    {
        "query": "退改",
        "content": "如果您需要人工服务，可以拨打人工客服电话：4006660921"}]
          }'
          
```







### 搜索知识库并回复答案

search_chat_llm

```bash
curl -X POST http://127.0.0.1:5000/search_chat_llm \
     -H "Content-Type: application/json" \
     -d '{"name": "unStructured111",
          "query": "管理项目知识输入为哪些内容"
          }'
          
        
 logger - INFO - query: 管理项目知识输入为哪些内容,answer:管理项目知识的输入内容如下：
1. 项目管理计划；
2. 项目文件（经验教训登记册、项目团队派工单、资源分解结构、供方选择标准、相关方登记册）；
3. 可交付成果；
4. 事业环境因素；
5. 组织过程资产。

curl -X POST http://127.0.0.1:6000/search_chat_llm \
     -H "Content-Type: application/json" \
     -d '{"name": "test_0087",
          "query": "请你介绍一下软通动力信息技术（集团）股份有限公司"
          }'

curl -X POST http://127.0.0.1:6000/chat \
     -H "Content-Type: application/json" \
     -d '{"name": "test_0087",
          "query": "请你介绍一下软通动力信息技术（集团）股份有限公司"
          }'
          
curl -X POST http://127.0.0.1:6000/chat \
     -H "Content-Type: application/json" \
     -d '{"name": "test_0087",
          "query": "请你介绍一下软通动力信息技术（集团）股份有限公司"
          }'          
  
  curl -X POST http://127.0.0.1:8000/get_text \
     -H "Content-Type: application/json" \
     -d '{
          "message": [
              {"role": "system", "content": "你是一个智能助手。"},
              {"role": "user", "content": "头晕肚子不舒服怎么办"}
          ]
     }'

```



豆包推理

```
from volcenginesdkarkruntime import Ark

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)

# Non-streaming:
print("----- standard request -----")
completion = client.chat.completions.create(
    model="ep-20250102103726-d9hzb",
    messages = [
        {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
        {"role": "user", "content": "常见的十字花科植物有哪些？"},
    ],
    # 免费开启推理会话应用层加密，访问 https://www.volcengine.com/docs/82379/1389905 了解更多
    extra_headers={'x-is-encrypted': 'true'},
)
print(completion.choices[0].message.content)

# Streaming:
print("----- streaming request -----")
stream = client.chat.completions.create(
    model="ep-20250102103726-d9hzb",
    messages = [
        {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
        {"role": "user", "content": "常见的十字花科植物有哪些？"},
    ],
    # 免费开启推理会话应用层加密，访问 https://www.volcengine.com/docs/82379/1389905 了解更多
    extra_headers={'x-is-encrypted': 'true'},
    stream=True
)
for chunk in stream:
    if not chunk.choices:
        continue
    print(chunk.choices[0].delta.content, end="")
print()
```



#### 提取关键词和摘要

```bash
curl -X POST http://127.0.0.1:6000/graph_keywords \
     -H "Content-Type: application/json" \
     -d '{
          "query": "软通动力拥有软通咨询、软通金科、软通工业互联、软通数字能源、机械革命、清华同方、软通华方七大业务子品牌，并在全球40余个城市布局业务，构建北美、日本、东南亚、中东四大国际交付中心，在北京城市副中心、江苏苏州、江苏无锡建设三大智能制造工厂。同时，公司前瞻布局智能制造、ICT软硬基础能力和生产力智能化产品，打造产业链闭环。"
          }'
          
          
curl -X POST http://127.0.0.1:6000/graph_keywords \
     -H "Content-Type: application/json" \
     -d '{
          "query": "软通动力设立30个能力中心，拥有1个国家级工程实验室，6个省市政府认定的工程、技术实验室及研发中心，1个博士后科研工作站，50+技术合作伙伴的生态合作体系，不断探索前沿技术的巨大商业应用潜力。公司旗下教育品牌软通教育，拥有一家全日制本科学院——郑州西亚斯学院数字技术产业学院；同时在全国合作院校600多所，设有70多个校企联合人才培养基地，通过校企合作、协同育人，为社会培养高素质应用型人才。"
          }'
                  
  
```



关键词和摘要保存到向量数据库vectordb

```python
from vectordb import Memory

# 初始化Memory对象作为存储库
memory = Memory()

# 示例数据: 文本内容及其关联元数据
texts = ["软通动力信息技术（集团）股份有限公司（以下简称“软通动力”）是中国数字技术产品和服务创新领导企业，致力于成为一家具有全球影响力的科技企业，企业数字化转型可信赖合作伙伴。公司2005年成立于北京，多年来始终坚持科技创新，具有软硬全栈的智能技术产品和服务能力，提供软件与数字技术服务、计算产品与数字基础设施、数字能源与智算服务以及国际化服务。目前，公司在10余个重要行业服务超过1100家国内外客户，其中超过230家客户为世界500强或中国500强企业，员工近90000人",
         "软通动力拥有软通咨询、软通金科、软通工业互联、软通数字能源、机械革命、清华同方、软通华方七大业务子品牌，并在全球40余个城市布局业务，构建北美、日本、东南亚、中东四大国际交付中心，在北京城市副中心、江苏苏州、江苏无锡建设三大智能制造工厂。同时，公司前瞻布局智能制造、ICT软硬基础能力和生产力智能化产品，打造产业链闭环。",
         "软通动力设立30个能力中心，拥有1个国家级工程实验室，6个省市政府认定的工程、技术实验室及研发中心，1个博士后科研工作站，50+技术合作伙伴的生态合作体系，不断探索前沿技术的巨大商业应用潜力。公司旗下教育品牌软通教育，拥有一家全日制本科学院——郑州西亚斯学院数字技术产业学院；同时在全国合作院校600多所，设有70多个校企联合人才培养基地，通过校企合作、协同育人，为社会培养高素质应用型人才"]
metadatas = [[{"abstract": "软通动力信息技术（集团）股份有限公司成立于 2005 年，总部在北京，是中国数字技术产品和服务的创新领导者，致力于成为全球影响力的科技企业和数字化转型的可信赖合作伙伴，拥有多种服务能力且服务众多客户，员工近 90000 人",
               "high_level_keywords":"软通动力、中国数字技术、全球影响力、企业数字化转型",
               "low_level_keywords":"软硬全栈智能技术、软件数字技术服务、计算数字基础设施"}],
             [{"abstract": "软通动力拥有七大业务子品牌，在全球 40 余个城市布局业务，构建四大国际交付中心，在多地建设智能制造工厂，同时前瞻布局相关领域打造产业链闭环",
               "high_level_keywords":"软通动力、七大业务子品牌、全球业务布局、智能制造",
               "low_level_keywords":"""软通咨询", "软通金科", "软通工业互联", "软通数字能源", "机械革命", "清华同方", "软通华方", "全球 40 余个城市", "北美、日本、东南亚、中东四大国际交付中心", "北京城市副中心", "江苏苏州", "江苏无锡", "三大智能制造工厂", "智能制造", "ICT 软硬基础能力"""}],
[{"abstract": "软通动力设立多种研究和合作机构，拥有 30 个能力中心等，旗下教育品牌软通教育与多所院校合作，培养高素质应用型人才。",
  "high_level_keywords":"""软通动力", "能力中心", "国家级工程实验室", "省市政府认定实验室", "博士后科研工作站", "技术合作伙伴", "软通教育", "全日制本科学院", "校企合作", "协同育人""",
  "low_level_keywords":"""30 个能力中心", "1 个国家级工程实验室", "6 个省市政府认定实验室", "1 个博士后科研工作站", "50+技术合作伙伴", "郑州西亚斯学院数字技术产业学院", "600 多所合作院校", "70 多个校企联合人才培养基地"""}]
             ]

# 保存文本和元数据到Memory中，自动完成内容的嵌入
for text, meta in zip(texts, metadatas):
    memory.save(text, meta)

# 使用关键词查询，自动找到最相关的片段
query = "请你介绍一下软通的教育业务"
results = memory.search(query, top_n=1)
print("查询结果:", results)
```



#### 提取整个知识库的关键词和摘要

```bash
curl -X POST http://127.0.0.1:6000/extract_keywords_abstract \
     -H "Content-Type: application/json" \
     -d '{
          "name": "test_01"
          }'
          

curl -X POST http://127.0.0.1:6000/extract_keywords_abstract \
     -H "Content-Type: application/json" \
     -d '{
          "name": "tet"
          }'
```



#### milvus向量数据库

##### 1 创建collection

##### 2 保存 search 以及query

```python
from pymilvus import MilvusClient
import numpy as np
from volcenginesdkarkruntime import Ark
client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key= 'bbe6290f-800a-41bc-b6e7-5992f5e13ede',
        region ="cn-beijing"
)
print("----- embeddings request -----")
resp = client.embeddings.create(
    model="ep-20240821171722-zn25j", #接入点
    input=["花椰菜又称菜花、花菜，是一种常见的蔬菜。"]
)
print(resp.data)
print(len(resp.data[0].embedding))


client = MilvusClient("./milvus_demo.db")
client.create_collection(
    collection_name="demo_isoftstone",
    dimension=2560  # The vectors we will use in this demo has 384 dimensions
)

# Text strings to search from.
docs = [
    "软通动力信息技术（集团）股份有限公司（以下简称“软通动力”）是中国数字技术产品和服务创新领导企业，致力于成为一家具有全球影响力的科技企业，企业数字化转型可信赖合作伙伴。公司2005年成立于北京，多年来始终坚持科技创新，具有软硬全栈的智能技术产品和服务能力，提供软件与数字技术服务、计算产品与数字基础设施、数字能源与智算服务以及国际化服务。目前，公司在10余个重要行业服务超过1100家国内外客户，其中超过230家客户为世界500强或中国500强企业，员工近90000人。",
   "软通动力拥有软通咨询、软通金科、软通工业互联、软通数字能源、机械革命、清华同方、软通华方七大业务子品牌，并在全球40余个城市布局业务，构建北美、日本、东南亚、中东四大国际交付中心，在北京城市副中心、江苏苏州、江苏无锡建设三大智能制造工厂。同时，公司前瞻布局智能制造、ICT软硬基础能力和生产力智能化产品，打造产业链闭环。",
    "软通动力设立30个能力中心，拥有1个国家级工程实验室，6个省市政府认定的工程、技术实验室及研发中心，1个博士后科研工作站，50+技术合作伙伴的生态合作体系，不断探索前沿技术的巨大商业应用潜力。公司旗下教育品牌软通教育，拥有一家全日制本科学院——郑州西亚斯学院数字技术产业学院；同时在全国合作院校600多所，设有70多个校企联合人才培养基地，通过校企合作、协同育人，为社会培养高素质应用型人才。"
]
# For illustration, here we use fake vectors with random numbers (384 dimension).

vectors = [client.embeddings.create(model="ep-20240821171722-zn25j",  # 接入点
        input=[docs[i]]
    ).data[0].embedding for i in range(len(docs)) ]
data = [ {"id": i, "vector": vectors[i], "text": docs[i], "subject": "history"} for i in range(len(vectors)) ]
res = client.insert(
    collection_name="demo_isoftstone",
    data=data
)

# This will exclude any text in "history" subject despite close to the query vector.
res = client.search(
    collection_name="demo_isoftstone",
    data=[vectors[0]],
    filter="subject == 'history'",
    limit=2,
    output_fields=["text", "subject"],
)
print(res)

# a query that retrieves all entities matching filter expressions.
res = client.query(
    collection_name="demo_isoftstone",
    filter="subject == 'history'",
    output_fields=["text", "subject"],
)
print(res)

# delete
res = client.delete(
    collection_name="demo_isoftstone",
    filter="subject == 'history'",
)
print(res)
```



#### 结合关键词和摘要对知识库进行检索重排(new)



平替GraphRAG

https://github.com/NanGePlus/GraphragTest



https://github.com/gusye1234/nano-graphrag















```
curl https://ark.cn-beijing.volces.com/api/v3/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ea764f0f-3b60-45b3-****-************" \
  -d '{
    "model": "ep-20240704******-*****",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Hello!"
        }
    ]
  }'
```





#### 创建 Session 缓存

```curl
curl --location 'https://ark.cn-beijing.volces.com/api/v3/context/create' \
--header 'Authorization: Bearer f62bafd2-1269-4169-b072-7994b36541a7' \
--header 'Content-Type: application/json' \
--data '{ 
    "model":"ep-20250120174411-9h98m", 
    "messages":[ 
        {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
        {"role": "user", "content": "常见的十字花科植物有哪些？"}
     ], 
     "ttl":3600, 
     "mode": "session"
}'


{"id":"ctx-20250120174458-6c94p","model":"ep-20250120174411-9h98m","ttl":5600,"truncation_strategy":{"type":"rolling_tokens","rolling_tokens":true},"usage":{"prompt_tokens":18,"completion_tokens":0,"total_tokens":18,"prompt_tokens_details":{"cached_tokens":0}},"mode":"session"}
```

#### 使用 Session 缓存进行对话

我们使用接口[ContextChatCompletions-上下文缓存对话](https://www.volcengine.com/docs/82379/1346560)，来进行使用 Session 缓存的对话

```
curl --location 'https://ark.cn-beijing.volces.com/api/v3/context/chat/completions' \
--header 'Authorization: Bearer f62bafd2-1269-4169-b072-7994b36541a7' \
--header 'Content-Type: application/json' \
--data '{
    "context_id": "ctx-20250120174458-6c94p",
    "model": "ep-20250120174411-9h98m",
    "messages":[
        {
            "role":"user",
            "content": "你好,请你介绍一下软通动力"
        }
    ]
}'



curl --location 'https://ark.cn-beijing.volces.com/api/v3/context/create' \
--header 'Authorization: Bearer f62bafd2-1269-4169-b072-7994b36541a7' \
--header 'Content-Type: application/json' \
--data '{ 
    "model":"ep-20250120174411-9h98m", 
    "messages":[ 
        {"role":"system","content":"你是李雷，你只会说“我是李雷”"}
     ], 
     "ttl":3600, 
     "mode": "session"
     {
     "truncation_strategy":{
         "type": "last_history_tokens",
         "last_history_tokens": 8192
    }
}'
```



### 下载数据集 bash download-dataset.sh train 499

https://p9-dcd-sign.byteimg.com/tos-cn-i-f042mdwyw7/d394532c8c38400e88f06e375ef1f0ec~tplv-f042mdwyw7-auto-webp:640:0.jpg?rk3s=23c6fcc1&x-expires=1744095606&x-signature=CmczdQFM%2BrCKP0wEtBdN4oPYdJk%3D&psm=motor.business.sku_item



# 懂车拍

## 点位分析

```
 {'model_1': 'doubao', 'model_2': 'zhipuai', 'model_3': 'deepseek'}
 
curl -X POST http://127.0.0.1:4000/Dianwei \
     -H "Content-Type: application/json" \
     -d '{"text": "分析一下这张图片",
          "url": "https://p9-dcd-sign.byteimg.com/tos-cn-i-f042mdwyw7/2c83169a46a949b3b319793094152576~tplv-f042mdwyw7-auto-webp:640:0.jpg?rk3s=23c6fcc1&x-expires=1744095606&x-signature=JyKGFGqnCw%2FeVx8QGlXTsz8ZZgM%3D&psm=motor.business.sku_item"
         }'
         
         
curl -X POST http://118.145.187.17:4000/Dianwei \
     -H "Content-Type: application/json" \
     -d '{"text": "分析一下这张图片",
     		"model_type": "model_1",
          "url": "https://p9-dcd-sign.byteimg.com/tos-cn-i-f042mdwyw7/2c83169a46a949b3b319793094152576~tplv-f042mdwyw7-auto-webp:640:0.jpg?rk3s=23c6fcc1&x-expires=1744095606&x-signature=JyKGFGqnCw%2FeVx8QGlXTsz8ZZgM%3D&psm=motor.business.sku_item"
         }'         
```

