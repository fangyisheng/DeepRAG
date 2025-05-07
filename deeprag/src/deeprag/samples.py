from deeprag.core import DeepRAG
from deeprag.workflow.data_model import KnowledgeScopeLocator
import asyncio
from typing import Any
import traceback
from io import BytesIO
import asyncio
from loguru import logger

deeprag = DeepRAG()


async def create_user(user_name: str):
    create_user = await deeprag.create_user(user_name)
    return create_user


async def create_knowledge_space(
    user_id: str,
    knowledge_space_name: str,
):
    created_knowledge_space = await deeprag.create_knowledge_space(
        user_id, knowledge_space_name
    )
    return created_knowledge_space


async def create_file_and_upload_to_minio(
    knowledge_space_id: str,
    bucket_name: str,
    object_name: str,
    file_path: str | None = None,
    string_data: str | None = None,
    io_data: BytesIO | None = None,
    metadata: dict | None = None,
):
    knowledge_scope_minio_mapping = await deeprag.create_file_and_upload_to_minio(
        knowledge_space_id=knowledge_space_id,
        bucket_name=bucket_name,
        object_name=object_name,
        file_path=file_path,
    )
    return knowledge_scope_minio_mapping


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


async def batch_index(
    collection_name: str,
    knowlege_scope: list[KnowledgeScopeLocator] | KnowledgeScopeLocator,
    deep_index_pattern: bool = False,
):
    await deeprag.batch_index(
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


# 业务流程开始，先跑一遍全流程


async def main(
    user_name: str,
    knowledge_space_name: str,
    file_path: str,
    collection_name: str,
    deep_index_pattern: bool,
    deep_query_pattern: bool,
    minio_bucket_name: str,
    minio_object_name: str,
    user_prompt: str,
    session_id: str,
    stream: bool,
):
    user = await create_user(user_name=user_name)
    logger.info(user)
    knowledge_space = await create_knowledge_space(
        user_id=user.id, knowledge_space_name=knowledge_space_name
    )
    logger.info(knowledge_space)
    file = await create_file_and_upload_to_minio(
        knowledge_space_id=knowledge_space.id,
        bucket_name=minio_bucket_name,
        object_name=minio_object_name,
        file_path=file_path,
    )
    knowledge_scope = KnowledgeScopeLocator(
        user_id=user.id,
        knowledge_space_id=knowledge_space.id,
        file_id=file.knowledge_scope.file_id,
    )

    await index(
        collection_name=collection_name,
        knowlege_scope=knowledge_scope,
        deep_index_pattern=deep_index_pattern,
    )
    result = await query(
        user_prompt=user_prompt,
        knowledge_scope=knowledge_scope,
        deep_query_pattern=deep_query_pattern,
        session_id=session_id,
        stream=stream,
    )
    if stream:
        async for chunk in result:
            print(chunk)
    else:
        print(result)


# 如果stream=True，则返回SSE的数据流，如果stream=False，则返回一个字典（其中包含回答）
# 对于SSE数据更推荐使用postman或者apifox的API测试来查看数据
print(
    asyncio.run(
        main(
            user_name="test",
            knowledge_space_name="test",
            file_path="/home/easonfang/DeepRAG/deeprag/src/deeprag/knowledge_file/test2.txt",
            collection_name="test_collection",
            deep_index_pattern=True,
            deep_query_pattern=True,
            minio_bucket_name="test",
            minio_object_name="test2.txt",
            user_prompt="深度求索的产业生态怎么样？",
            session_id="",
            stream=True,
        )
    )
)

# 如果已经创建好了user空间和knowledge_space空间，想要做batch_index的过程，那么参考如下的操作


async def batch_index_process(
    knowledge_scope: KnowledgeScopeLocator,
    collection_name: str,
    deep_index_pattern: bool = False,
):
    result = await batch_index(
        collection_name=collection_name,
        knowledge_scope=knowledge_scope,
        deep_index_pattern=deep_index_pattern,
    )
