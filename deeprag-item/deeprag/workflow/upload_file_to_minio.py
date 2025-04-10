from deeprag.rag_core_utils.s3_api.s3_api_client import create_minio_client
from deeprag.workflow.data_model import UploadFileToMinioResponse


async def upload_file_to_minio_func(
    bucket_name, file_path, object_name
) -> UploadFileToMinioResponse:
    client = await create_minio_client()

    # 检查存储桶是否存在，如果不存在则创建
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    # 上传文件
    uploaded_file_object = client.fput_object(
        bucket_name=bucket_name, object_name=object_name, file_path=file_path
    )

    return UploadFileToMinioResponse(
        **{
            "status": "success" if uploaded_file_object else "failed",
            "minio_upload_result": uploaded_file_object,
        }
    )


# #测试通过
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
