from deeprag.rag_core_utils.vector_db_api.vector_db_api_client import (
    create_or_use_hybrid_search_milvus_client_collection,
)
from loguru import logger


# 这边按道理会插入稀疏向量和稠密向量 BM25算法会自动生成sparse的稀疏向量
async def data_insert_to_vector_db(
    text_list: list,
    vector: list,
    collection_name: str,
    partition_name: str,
    meta_data: list | None = None,
):
    # 通过引入字典解包，实现动态键值对的增加
    data = [
        {
            "text": text_list[i],
            "dense": vector[i],
            **({"meta_data": meta_data[i]} if meta_data else {}),
        }
        for i in range(len(text_list))
    ]
    logger.info(f"{data}")
    client = await create_or_use_hybrid_search_milvus_client_collection(collection_name)

    res = client.insert(collection_name="test", data=data)
    return res
