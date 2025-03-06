from deeprag.rag_core_utils.vector_db_api.vector_db_api_client import create_hybrid_search_milvus_client_collection

#这边按道理会插入稀疏向量和稠密向量 BM25算法会自动生成sparse的稀疏向量
async def data_insert_to_vector_db(text_chunk_list,vector,meta_data):
    data = [{"id":i,
             "text": text_chunk_list[i],
             "dense":vector[i],
             "meta_data":meta_data[i]} 
             for i in range(text_chunk_list)]
    client = await create_hybrid_search_milvus_client_collection()

    res = client.insert(
    collection_name="test",
    data=data
     )
    return res
