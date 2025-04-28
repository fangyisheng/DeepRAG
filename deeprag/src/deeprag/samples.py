from deeprag.core import DeepRAG
from deeprag.workflow.data_model import KnowledgeScopeLocator
import asyncio
from typing import Any


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


async def index(collection_name: str, knowlege_scope: KnowledgeScopeLocator):
    await deeprag.index(
        collection_name=collection_name,
        knowledge_scope=knowlege_scope,
        deep_index_pattern=False,
    )


async def query_non_stream(
    user_prompt: str,
    collection_name: str,
    knowlege_scope: KnowledgeScopeLocator,
    session_id: str | None = None,
):
    response_answer = await deeprag.query_answer_non_stream(
        user_prompt=user_prompt,
        collection_name=collection_name,
        knowledge_scope=knowlege_scope,
        deep_query_pattern=False,
        session_id=session_id,
    )
    return response_answer


import asyncio


async def main():
    await created_knowledge_scope(
        user_name="test_name",
        knowledge_space_name="test_knowledge_space",
        minio_bucket_name="mybucket",
        minio_object_name="test1.txt",
        file_path="/home/easonfang/DeepRAG/deeprag/src/deeprag/samples.py",
    )


print(asyncio.run(main()))
