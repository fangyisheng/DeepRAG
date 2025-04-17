from deeprag.deeprag import DeepRAG
import asyncio

deeprag = DeepRAG()


async def main(file_path: str):
    created_user = await deeprag.create_user("test_user")
    created_knowledge_space = await deeprag.create_knowledge_space(
        created_user.id, "test_knowledge_space"
    )
    created_file = await deeprag.create_file_and_upload_to_minio(
        file_path, created_knowledge_space.id, "mybucket", "test1.txt"
    )
    await deeprag.index(
        "test_collection",
        created_file.knowledge_scope,
        meta_data="test_meta_data",
        deep_index_pattern=False,
    )
    response_answer = await deeprag.query_answer_non_stream(
        user_prompt="深度求索和哪些公司产生了合作关系？",
        collection_name="test_collection",
        knowledge_scope=created_file.knowledge_scope,
        deep_query_pattern=False,
    )
    return response_answer
