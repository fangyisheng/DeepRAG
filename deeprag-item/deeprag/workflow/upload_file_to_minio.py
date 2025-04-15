from deeprag.rag_core_utils.s3_api.s3_api_client import create_minio_client
from deeprag.workflow.data_model import UploadFileToMinioResponse
from io import BytesIO


async def upload_file_to_minio_func(
    bucket_name: str,
    object_name: str,
    file_path: str | None = None,
    string_data: str | None = None,
) -> UploadFileToMinioResponse:
    client = await create_minio_client()

    # 检查存储桶是否存在，如果不存在则创建
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    # 上传文件
    if file_path and not string_data:
        uploaded_file_object = client.fput_object(
            bucket_name=bucket_name, object_name=object_name, file_path=file_path
        )

    if string_data and not file_path:
        uploaded_file_object = client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=BytesIO(string_data.encode("utf-8")),
            length=len(string_data.encode("utf-8")),
        )

    return UploadFileToMinioResponse(
        **{
            "status": "success" if uploaded_file_object else "failed",
            "minio_upload_result": uploaded_file_object,
        }
    )


# # 测试上传本地文件路径的代码
# import asyncio

# print(
#     asyncio.run(
#         upload_file_to_minio_func(
#             "mybucket",
#             "/home/easonfang/DeepRAG/deeprag-item/deeprag/knowledge_file/test.txt",
#             "test.txt",
#         )
#     )
# )

# # 测试上传数据流的代码
# import asyncio

# print(
#     asyncio.run(
#         upload_file_to_minio_func(
#             bucket_name="mybucket",
#             object_name="test3.txt",
#             string_data="nihao",
#         )
#     )
# )
