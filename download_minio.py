from minio import Minio
from datetime import datetime, timedelta, timezone

# 创建 Minio 客户端
client = Minio("118.145.187.17:9000",
    access_key="minioadmin",
    secret_key="minioadmin", secure=False
)
# 列出所有存储桶
print(client.list_buckets())
bucket_name = "dcar1000"
#client.fput_object(
#        bucket_name, 'infer.py', 'infer.py',
#    )
#client.fget_object("caijian", "ollama-linux-amd64.tgz", "ollama-linux-amd64.tgz")

#client.fput_object("caijian", "checkpoint-124.zip", "checkpoint-124.zip")
client.fget_object("dcar1000", "ms-swift-main.zip", "ms-swift-main.zip")
#client.fget_object("caijian", "Dcar_1000_test.json", "Dcar_1000_test.json")
#client.fget_object("caijian", "car_train.py", "car_train.py")
#client.fget_object("caijian", "csv2json.py", "csv2json.py")

