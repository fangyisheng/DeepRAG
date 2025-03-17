from minio import Minio
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()


minio_secure = os.getenv("MINIO_SECURE")

if minio_secure == "False":
    minio_secure = False
else:
    minio_secure = True


# async def create_minio_client():
#     client = Minio(
#         "127.0.0.1:9000",  # MinIO 服务器地址和端口
#         access_key="minioadmin",  # 替换为你的 Access Key
#         secret_key="minioadmin",  # 替换为你的 Secret Key
#         secure=os.getenv("MINIO_SECURE"),  # 如果使用 HTTPS，则设置为 True
#     )
#     return client


# print(asyncio.run(create_minio_client()))


if not minio_secure:
    print("nihao")
print(type(os.getenv("MINIO_SECURE")))

print(bool("False"))
