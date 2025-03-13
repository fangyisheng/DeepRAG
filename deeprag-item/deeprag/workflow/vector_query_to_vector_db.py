from deeprag.rag_core_utils.vector_db_api.vector_db_api_client import (
    create_or_use_hybrid_search_milvus_client_collection_partition,
)
from deeprag.rag_core_utils.embedding_api.embedding_api_client import text_to_vector
from pymilvus import AnnSearchRequest
from pymilvus import RRFRanker
from loguru import logger


async def query_vector_db_by_vector(query, collection_name, partition_name):
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
    client = await create_or_use_hybrid_search_milvus_client_collection_partition(
        collection_name, partition_name
    )
    res = client.hybrid_search(
        collection_name=collection_name,
        reqs=reqs,
        ranker=ranker,
        limit=2,
        output_fields=["text", "meta_data"],
        partition_names=[partition_name],
    )
    context = [item["entity"]["text"] for item in res[0]]
    return context
