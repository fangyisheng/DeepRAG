from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from minio import Minio
from pathlib import Path
from typing import Dict
import os
import json


def upload_file_to_minio(file_stream, file_name, file_length):
    # 初始化客户端
    client = Minio(
        "localhost:9002", access_key="minioadmin", secret_key="minioadmin", secure=False
    )
    bucket_name = "mybucket"
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        print(f"Bucket '{bucket_name}' created successfully.")
    else:
        print(f"Bucket '{bucket_name}' already exists.")
    client.put_object(
        "mybucket", file_name, file.file, length=os.fstat(file.file.fileno()).st_size
    )


app = FastAPI()


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), metadata: str = Form(...)):
    upload_file_to_minio(file)
    return {
        "filename": file.filename,
        "metadata": json.loads(metadata),  # 返回解析后的字典
    }


# 文件上传系统和字段测试通过，要狠狠地理解依赖注入啊！！！！！
