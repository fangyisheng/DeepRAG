from deeprag.rag_core_utils.vector_db_api.vector_db_api_client import client

async def data_insert_to_vector_db(text_chunk,vector,meta_data):
    data = [{"id":i,"vector":vector[i],"meta_data": meta_data[i]} for i in range(text_chunk)]
    res = client.insert(
    collection_name="test",
    data=data
)
    return res
