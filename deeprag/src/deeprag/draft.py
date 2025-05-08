from deeprag.samples import (
    batch_index,
    batch_create_file_and_upload_to_minio_process,
    create_file_and_upload_to_minio,
    create_knowledge_space,
    create_user,
    index,
    query,
)


import asyncio

# asyncio.run(
#     create_knowledge_space(
#         user_id="e7a6aec2-f7d8-4911-be92-1947c8343975",
#         knowledge_space_name="knowledge_space_2",
#     )
# )

asyncio.run(
    batch_create_file_and_upload_to_minio_process(
        knowledge_space_id="7b9acca8-a265-4aca-8e6f-444072586580",
        bucket_name_list=["mybucket", "mybucket"],
        object_name_list=["test.csv", "test2.txt"],
        file_path_list=[
            "/home/easonfang/DeepRAG/deeprag/src/deeprag/knowledge_file/test.csv",
            "/home/easonfang/DeepRAG/deeprag/src/deeprag/knowledge_file/test2.txt",
        ],
    )
)
