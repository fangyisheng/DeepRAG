from deeprag.rag_core_utils.vector_db_api.vector_db_api_client import (
    create_or_use_hybrid_search_milvus_client_collection,
)
from loguru import logger

from deeprag.workflow.data_model import (
    DataInsertVectorDBResponse,
    KnowledgeScopeLocator,
)


# 这边按道理会插入稀疏向量和稠密向量 BM25算法会自动生成sparse的稀疏向量
async def data_insert_to_vector_db(
    text_list: list,
    vector: list,
    collection_name: str,
    knowledge_scope: list[KnowledgeScopeLocator],
    community_cluster: list | None = None,
    meta_data: list | None = None,
) -> DataInsertVectorDBResponse:
    """
    knowledge_scope 的列表元素举例
    {
      "user_id":"",
      "knowledge_space_id":"",
      "file_id":""
    }

    community_cluster 举例：
    [uuid, uuid, uuid, uuid]
    """
    # 通过引入字典解包，实现动态键值对的增加
    knowledge_scope_list = [item.model_dump() for item in knowledge_scope]
    data = [
        {
            "text": text_list[i],
            "dense": vector[i],
            "knowledge_scope": knowledge_scope_list[i],
            "meta_data": meta_data[i] if meta_data else "",
            "community_id": community_cluster[i] if community_cluster else "",
        }
        for i in range(len(text_list))
    ]
    client = await create_or_use_hybrid_search_milvus_client_collection(collection_name)

    res = client.insert(collection_name=collection_name, data=data)
    # return {
    #     "status": "success" if res else "failed",
    #     "inserted_count": len(data),
    #     "collection": collection_name,
    #     "zilliz_response": res,  # 保留原始响应
    # }
    return DataInsertVectorDBResponse(
        status="success" if res else "failed",
        inserted_count=len(data),
        collection_name=collection_name,
        zilliz_response=res,  # 保留原始响应
    )
