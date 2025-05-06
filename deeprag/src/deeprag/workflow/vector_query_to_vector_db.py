from deeprag.rag_core_utils.vector_db_api.vector_db_api_client import (
    create_or_use_hybrid_search_milvus_client_collection,
)
from deeprag.rag_core_utils.embedding_api.embedding_api_client import text_to_vector
from pymilvus import AnnSearchRequest
from pymilvus import RRFRanker
from deeprag.workflow.data_model import SearchedTextResponse, KnowledgeScopeLocator
from loguru import logger


async def query_vector_db_by_vector(
    query: str,
    collection_name: str,
    knowledge_scope: KnowledgeScopeLocator,
    recalled_text_fragments_top_k: int,
    deep_query_pattern: bool = False,
) -> SearchedTextResponse:
    # user_id = knowledge_scope.get("user_id")
    # knowledge_space_id = knowledge_scope.get("knowledge_space_id")
    # file_id = knowledge_scope.get("file_id")
    valid_keys = []
    for key in ("user_id", "knowledge_space_id", "file_id"):
        value = knowledge_scope.model_dump().get(key)
        if value:
            valid_keys.append(key)
    last_key = valid_keys[-1]
    last_value = knowledge_scope.model_dump().get(last_key)
    if last_key == "user_id":
        filter = f"""knowledge_scope["{last_key}"] == "{last_value}" """
    elif last_key == "knowledge_space_id":
        filter = f"""knowledge_scope["{last_key}"] == "{last_value}" """
    elif last_key == "file_id":
        filter = f"""knowledge_scope["{last_key}"] == "{last_value}" """
    query_vector = await text_to_vector([query])
    if deep_query_pattern:
        filter = filter + ' AND commuity_id != ""'
    else:
        filter = filter + ' AND commuity_id == ""'
    # filter = 'knowledge_scope["file_id"] == "e6edc631-1b3e-436c-9888-4b6d1f84a706" AND community_id !=""'
    logger.info(f"这是zilliz的筛选条件{filter}")
    search_param_1 = {
        "data": query_vector.embedding_vector,
        "anns_field": "dense",
        "param": {"metric_type": "IP", "params": {"nprobe": 10}},
        "limit": recalled_text_fragments_top_k,
        "expr": filter,
    }
    request_1 = AnnSearchRequest(**search_param_1)
    search_param_2 = {
        "data": [query],
        "anns_field": "sparse",
        "param": {"metric_type": "BM25", "params": {"drop_ratio_build": 0.2}},
        "limit": recalled_text_fragments_top_k,
        "expr": filter,
    }

    request_2 = AnnSearchRequest(**search_param_2)
    reqs = [request_1, request_2]
    ranker = RRFRanker()
    client = await create_or_use_hybrid_search_milvus_client_collection(collection_name)
    res = client.hybrid_search(
        collection_name=collection_name,
        reqs=reqs,
        ranker=ranker,
        limit=recalled_text_fragments_top_k,
        output_fields=["text", "meta_data", "knowledge_scope"],
    )
    logger.info(res)
    context = [item["entity"]["text"] for item in res[0]]
    return SearchedTextResponse(root=context)


# async def main():
#     result = await query_vector_db_by_vector(
#         query="当前深度求索技术的产业生态是怎样的？",
#         collection_name="test_collection",
#         knowledge_scope=KnowledgeScopeLocator(
#             user_id="c6fc9b5c-439b-4af5-8ac8-8540d384e2e6",
#             knowledge_space_id="3de5bcd0-ccd8-4cf3-8583-02c71ca51ac1",
#             file_id="e6edc631-1b3e-436c-9888-4b6d1f84a706",
#         ),
#         recalled_text_fragments_top_k=5,
#         deep_query_pattern=True,
#     )
#     return result


# import asyncio

# print(asyncio.run(main()))
