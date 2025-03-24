from minio import Minio


async def create_minio_client() -> "Minio":
    client = Minio(
        "127.0.0.1:9000",  # MinIO 服务器地址和端口
        access_key="minioadmin",  # 替换为你的 Access Key
        secret_key="minioadmin",  # 替换为你的 Secret Key
        secure=False,  # 如果使用 HTTPS，则设置为 True
    )
    return client
