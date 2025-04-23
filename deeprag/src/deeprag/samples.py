from deeprag.core import DeepRAG
from deeprag.workflow.data_model import KnowledgeScopeLocator
import asyncio

deeprag = DeepRAG()


async def created_knowledge_scope(
    user_name: str,
    knowledge_space_name: str,
    minio_bucket_name: str,
    minio_object_name: str,
    file_path: str,
) -> KnowledgeScopeLocator:
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

asyncio.run(
    query_non_stream(
        "深度求索和哪些公司有关系？",
        "test_collection",
        KnowledgeScopeLocator(
            user_id="d1e48bb5-f65c-4975-a667-4d68e01c67c1",
            knowledge_space_id="8bb5493d-32a2-47fa-b724-678ecbd04e25",
            file_id="49302933-e63d-4b79-8923-c5c31883f5b1",
        ),
    )
)
