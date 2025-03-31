from deeprag.rag_core_utils.vector_db_api.vector_db_api_client import (
    create_or_use_hybrid_search_milvus_client_collection,
)
from deeprag.rag_core_utils.embedding_api.embedding_api_client import text_to_vector
from pymilvus import AnnSearchRequest
from pymilvus import RRFRanker
from deeprag.workflow.data_model import SearchedTextResponse, KnowledgeScope


async def query_vector_db_by_vector(
    query: str, collection_name: str, knowledge_scope: KnowledgeScope
) -> SearchedTextResponse:
    # user_id = knowledge_scope.get("user_id")
    # knowledge_space_id = knowledge_scope.get("knowledge_space_id")
    # file_id = knowledge_scope.get("file_id")
    valid_keys = []
    for key in ("user_id", "knowledge_space_id", "file_id"):
        value = knowledge_scope.get(key)
        if value:
            valid_keys.append(key)
    last_key, last_value = valid_keys[-1]
    if last_key == "user_id":
        filter = f"""json_contains(knowledge_scope[{last_value}])"""
    elif last_key == "knowledge_space_id":
        filter = f"""json_contains(knowledge_scope[{last_value}])"""
    elif last_key == "file_id":
        filter = f"""json_contains(knowledge_scope[{last_value}])"""
    query_vector = await text_to_vector([query])
    search_param_1 = {
        "data": query_vector,
        "anns_field": "dense",
        "param": {"metric_type": "IP", "params": {"nprobe": 10}},
        "limit": 2,
    }
    request_1 = AnnSearchRequest(**search_param_1)
    search_param_2 = {
        "data": [query],
        "anns_field": "sparse",
        "param": {"metric_type": "BM25", "params": {"drop_ratio_build": 0.2}},
        "limit": 2,
    }

    request_2 = AnnSearchRequest(**search_param_2)
    reqs = [request_1, request_2]
    ranker = RRFRanker()
    client = await create_or_use_hybrid_search_milvus_client_collection(collection_name)
    res = client.hybrid_search(
        collection_name=collection_name,
        reqs=reqs,
        ranker=ranker,
        filter=filter,
        limit=2,
        output_fields=["text", "meta_data"],
    )
    context = [item["entity"]["text"] for item in res[0]]
    return context
