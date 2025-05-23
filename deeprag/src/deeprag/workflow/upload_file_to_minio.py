from deeprag.rag_core_utils.s3_api.s3_api_client import create_minio_client
from deeprag.workflow.data_model import UploadFileToMinioResponse
from io import BytesIO


async def upload_file_to_minio_func(
    bucket_name: str,
    object_name: str,
    file_path: str | None = None,
    string_data: str | None = None,
    io_data: BytesIO | None = None,
    metadata: dict | None = None,
) -> UploadFileToMinioResponse:
    client = await create_minio_client()

    # 检查存储桶是否存在，如果不存在则创建
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    # 上传文件
    if file_path and not string_data and not io_data:
        uploaded_file_object = client.fput_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=file_path,
            metadata=metadata,
        )

    if string_data and not file_path and not io_data:
        uploaded_file_object = client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=BytesIO(string_data.encode("utf-8")),
            length=len(string_data.encode("utf-8")),
            metadata=metadata,
        )
    if io_data and not string_data and not file_path:
        uploaded_file_object = client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=BytesIO(io_data),
            length=len(io_data),
            metadata=metadata,
        )

    return UploadFileToMinioResponse(
        **{
            "status": "success" if uploaded_file_object else "failed",
            "minio_upload_result": uploaded_file_object,
        }
    )


# 测试上传本地文件路径的代码,测试成功
# import asyncio

# print(
#     asyncio.run(
#         upload_file_to_minio_func(
#             bucket_name="mybucket",
#             file_path="DeepRAG/deeprag/src/deeprag/knowledge_file/test.txt",
#             object_name="test.txt",
#         )
#     )
# )

# # 测试上传数据流的代码,测试成功
# import asyncio

# print(
#     asyncio.run(
#         upload_file_to_minio_func(
#             bucket_name="mybucket",
#             object_name="test4.txt",
#             string_data="nihao",
#         )
#     )
# )
