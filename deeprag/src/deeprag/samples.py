from deeprag.core import DeepRAG
from deeprag.workflow.data_model import KnowledgeScopeLocator
import asyncio
from typing import Any
import traceback

deeprag = DeepRAG()


async def created_knowledge_scope(
    user_name: str,
    knowledge_space_name: str,
    minio_bucket_name: str,
    minio_object_name: str,
    file_path: str,
) -> Any:
    created_user = await deeprag.create_user(user_name)
    created_knowledge_space = await deeprag.create_knowledge_space(
        created_user.id, knowledge_space_name
    )
    created_file = await deeprag.create_file_and_upload_to_minio(
        file_path=file_path,
        knowledge_space_id=created_knowledge_space.id,
        bucket_name=minio_bucket_name,
        object_name=minio_object_name,
    )
    knowledge_scope = created_file.knowledge_scope
    return knowledge_scope


async def index(
    collection_name: str,
    knowlege_scope: KnowledgeScopeLocator,
    deep_index_pattern: bool = False,
):
    await deeprag.index(
        collection_name=collection_name,
        knowledge_scope=knowlege_scope,
        deep_index_pattern=deep_index_pattern,
    )


async def query(
    user_prompt: str,
    knowledge_scope: KnowledgeScopeLocator,
    deep_query_pattern: bool = False,
    session_id: str | None = None,
    stream: bool = False,
):
    if stream:
        response_answer = deeprag.query_by_stream(
            user_prompt=user_prompt,
            knowledge_scope=knowledge_scope,
            deep_query_pattern=deep_query_pattern,
            session_id=session_id,
        )
    else:
        response_answer = await deeprag.query_by_non_stream(
            user_prompt=user_prompt,
            knowledge_scope=knowledge_scope,
            deep_query_pattern=deep_query_pattern,
            session_id=session_id,
        )
    return response_answer


import asyncio


# async def main():
#     await created_knowledge_scope(
#         user_name="test_name",
#         knowledge_space_name="test_knowledge_space",
#         minio_bucket_name="mybucket",
#         minio_object_name="test1.txt",
#         file_path="/home/easonfang/DeepRAG/deeprag/src/deeprag/knowledge_file/test2.txt",
#     )


# async def main():
#     await index(
#         collection_name="test_collection",
#         knowlege_scope=KnowledgeScopeLocator(
#             user_id="c6fc9b5c-439b-4af5-8ac8-8540d384e2e6",
#             knowledge_space_id="3de5bcd0-ccd8-4cf3-8583-02c71ca51ac1",
#             file_id="e6edc631-1b3e-436c-9888-4b6d1f84a706",
#         ),
#         deep_index_pattern=True,
#     )


# print(asyncio.run(main()))


async def main():
    try:
        answer = await query(
            user_prompt="你好",
            knowledge_scope=KnowledgeScopeLocator(
                user_id="c6fc9b5c-439b-4af5-8ac8-8540d384e2e6",
                knowledge_space_id="3de5bcd0-ccd8-4cf3-8583-02c71ca51ac1",
                file_id="e6edc631-1b3e-436c-9888-4b6d1f84a706",
            ),
            deep_query_pattern=True,
            stream=False,
        )
        # async for chunk in answer:
        #     print(chunk)
        print(answer)
    except Exception as e:
        print(e)
        print(traceback.format_exc())


print(asyncio.run(main()))
