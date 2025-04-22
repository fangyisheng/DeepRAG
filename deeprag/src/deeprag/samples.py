from deeprag.core import DeepRAG
import asyncio

deeprag = DeepRAG()


async def main(file_path: str, user_prompt: str):
    created_user = await deeprag.create_user("test_user")
    created_knowledge_space = await deeprag.create_knowledge_space(
        created_user.id, "test_knowledge_space"
    )
    created_file = await deeprag.create_file_and_upload_to_minio(
        file_path=file_path,
        knowledge_space_id=created_knowledge_space.id,
        bucket_name="mybucket",
        object_name="test2.txt",
    )
    await deeprag.index(
        collection_name="test_collection",
        knowledge_scope=created_file.knowledge_scope,
        deep_index_pattern=False,
    )
    response_answer = await deeprag.query_answer_non_stream(
        user_prompt=user_prompt,
        collection_name="test_collection",
        knowledge_scope=created_file.knowledge_scope,
        deep_query_pattern=False,
    )
    return response_answer


import asyncio

asyncio.run(
    main(
        "/root/project/DeepRAG/deeprag/src/deeprag/knowledge_file/test.txt",
        "套型总建筑面积计算应符合什么规定？",
    )
)
