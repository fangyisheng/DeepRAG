from deeprag.rag_core_utils.vector_db_api.vector_db_api_client import (
    create_or_use_hybrid_search_milvus_client_collection_partition,
)
from loguru import logger


# 这边按道理会插入稀疏向量和稠密向量 BM25算法会自动生成sparse的稀疏向量
async def data_insert_to_vector_db(
    text_chunk_list, vector, meta_data, collection_name, partition_name
):
    data = [
        {"text": text_chunk_list[i], "dense": vector[i], "meta_data": meta_data[i]}
        for i in range(len(text_chunk_list))
    ]
    logger.info(f"{data}")
    client = await create_or_use_hybrid_search_milvus_client_collection_partition(
        collection_name, partition_name
    )

    res = client.insert(collection_name="test", data=data)
    res = client.insert(collection_name="test", data=data)
    return res
