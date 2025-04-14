from deeprag.rag_core_utils.embedding_api.embedding_api_client import text_to_vector
from deeprag.rag_core_utils.embedding_api.embedding_api_client import (
    embedding_model_input_string_array_length,
)
import asyncio
from deeprag.workflow.data_model import BatchTextChunkGenerateEmbeddingsResponse


"""
这是对关系的描述的列表或者对社区检测报告的列表的嵌入。不是对文本分块的简单嵌入哦~
目前本项目DeepRAG中没有对原始文本分块嵌入的操作。
"""


async def batch_text_chunk_generate_embeddings_process(
    chunked_text_array: list[str],
    embedding_model_input_string_array_length: int = embedding_model_input_string_array_length,
) -> BatchTextChunkGenerateEmbeddingsResponse:
    if len(chunked_text_array) <= embedding_model_input_string_array_length:
        vector_array = await text_to_vector(chunked_text_array)
        return BatchTextChunkGenerateEmbeddingsResponse(root=vector_array)
    else:
        batches = [
            chunked_text_array[i : i + embedding_model_input_string_array_length]
            for i in range(
                0, len(chunked_text_array), embedding_model_input_string_array_length
            )
        ]
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
        final_result = [item for sublist in results for item in sublist]
        return BatchTextChunkGenerateEmbeddingsResponse(root=final_result)


# 编写测试代码,测试成功
# import asyncio


# a = asyncio.run(
#     batch_text_chunk_generate_embeddings_process(["你好", "我是", "一个", "机器人"])
# )
# print(a)
