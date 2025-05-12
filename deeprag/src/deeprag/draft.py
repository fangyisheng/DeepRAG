from deeprag.samples import (
    batch_index,
    batch_create_file_and_upload_to_minio_process,
    create_file_and_upload_to_minio,
    create_knowledge_space,
    create_user,
    index,
    query,
)
from deeprag.workflow.data_model import KnowledgeScopeLocator

import asyncio

# asyncio.run(create_user(user_name="user_1"))

# asyncio.run(
#     create_knowledge_space(
#         user_id="d53c17a9-3a1a-4c21-ab86-bd609242fe91",
#         knowledge_space_name="knowledge_space_3",
#     )
# )

# asyncio.run(
#     batch_create_file_and_upload_to_minio_process(
#         knowledge_space_id_or_id_list=[
#             "47c8aa05-3761-4254-a3eb-e8d6943eaf6a",
#             "2ef4d78f-ca1b-4ef3-ac24-0080eeb8bc57",
#         ],
#         bucket_name_list=["mybucket", "mybucket"],
#         object_name_list=["test.csv", "test2.txt"],
#         file_path_list=[
#             "/home/easonfang/DeepRAG/deeprag/src/deeprag/knowledge_file/test.csv",
#             "/home/easonfang/DeepRAG/deeprag/src/deeprag/knowledge_file/test2.txt",
#         ],
#     )
# )

# asyncio.run(
#     batch_index(
#         collection_name="test_collection",
#         knowlege_scope=KnowledgeScopeLocator(
#             user_id="d53c17a9-3a1a-4c21-ab86-bd609242fe91"
#         ),
#         deep_index_pattern=True,
#     )
# )

# 下面测试多轮对话


async def test():
    chat = await query(
        user_prompt="我刚刚是不是跟你打招呼了，如果有的话就回答一下，谢谢",
        knowledge_scope=KnowledgeScopeLocator(
            user_id="d53c17a9-3a1a-4c21-ab86-bd609242fe91",
            knowledge_space_id="47c8aa05-3761-4254-a3eb-e8d6943eaf6a",
            file_id="28051a25-2922-41e9-aaef-1158798bc220",
        ),
        stream=True,
        deep_query_pattern=True,
        session_id="ac956983-c0ca-4463-a4a2-acdf812e791b",
    )
    async for chunk in chat:
        print(chunk)


asyncio.run(test())
