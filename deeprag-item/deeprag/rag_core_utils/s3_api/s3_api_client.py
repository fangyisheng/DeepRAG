from minio import Minio
from dotenv import load_dotenv
import os

load_dotenv()


async def convert_str_false_to_bool_false(str_false: str) -> bool:
    if str_false == "False":
        return False
    else:
        return True


async def create_minio_client() -> "Minio":
    client = Minio(
        os.getenv("MINIO_ENDPOINT"),  # MinIO 服务器地址和端口
        access_key=os.getenv("MINIO_ACCESS_KEY"),  # 替换为你的 Access Key
        secret_key=os.getenv("MINIO_SECRET_KEY"),  # 替换为你的 Secret Key
        secure=await convert_str_false_to_bool_false(
            os.getenv("MINIO_SECURE")
        ),  # 如果使用 HTTPS，则设置为 True
    )
    return client
