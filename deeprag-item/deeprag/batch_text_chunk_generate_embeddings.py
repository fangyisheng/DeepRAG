from deeprag.embedding_api_client import text_to_vector
from deeprag.embedding_api_client import embedding_model_input_string_array_length
import asyncio


async def batch_text_chunk_generate_embeddings_process(chunked_text_array:str, embedding_model_input_string_array_length:int = embedding_model_input_string_array_length):
    if len(chunked_text_array) <= embedding_model_input_string_array_length:
        vector_array = await text_to_vector(chunked_text_array)
        return vector_array
    else:
        batches = [chunked_text_array[i:i + embedding_model_input_string_array_length] for i in range(0, len(chunked_text_array), embedding_model_input_string_array_length)]
        # if len(batches) <= embedding_model_rps:
        #     tasks = [text_to_vector(batch) for batch in batches]
        #     results = await asyncio.gather(*tasks)
        #     return results
        # else:
        #      sub_batch = [batches[i:i + embedding_model_rps] for i in range(0, len(batches), embedding_model_rps)]
             
        #      for batch in sub_batch:
        #          results = await asyncio.gather(*batch)
        tasks = [text_to_vector(batch) for batch in batches]
        results = await asyncio.gather(*tasks)
        return [item  for sublist in results for item in sublist]





