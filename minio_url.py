#coding:utf-8
from minio import Minio
from datetime import datetime, timedelta, timezone

# 创建 Minio 客户端
client = Minio("118.145.187.17:9000",
    access_key="minioadmin",
    secret_key="minioadmin", secure=False
)
# 列出所有存储桶
print(client.list_buckets())

# 生成永久下载链接
bucket_name = "caijian"
object_name = "Agent.txt"
expiry = datetime.now(timezone.utc) + timedelta(days=7)  # 过期时间为7天
# 将过期时间转换为 timedelta 对象
expires_in = timedelta(seconds=int((expiry - datetime.now(timezone.utc)).total_seconds()))
# 生成预签名的下载URL
url = client.presigned_get_object(bucket_name, object_name, expires=expires_in)
# 打印URL
print(url)

# minio_client =Minio(
#     's3.amazonas.com',
#     access_key='access_key',
#     secret_key='secret_key',
#     secure=True
# )
# #生成永久下载链接
# bucket_name =" my-bucket"
# object_name ="my_object"
# expiry =datetime.utcnow() +timedelta(days=7) #过期时间为7天
# url =minio_client.presigned_get_object(bucket_name, object_name,expires=expiry)
# print(url) #为使用的对象生成永久下载链接