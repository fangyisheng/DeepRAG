from deeprag.rag_core_utils.embedding_api.embedding_api_client import text_to_vector
from deeprag.rag_core_utils.embedding_api.embedding_api_client import (
    embedding_model_input_string_array_length,
)
import asyncio
from deeprag.workflow.data_model import BatchTextChunkGenerateEmbeddingsResponse
from tqdm.asyncio import tqdm_asyncio
from deeprag.rag_core_utils.utils.context_holder import (
    embedding_token_usage_var,
)

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
        return BatchTextChunkGenerateEmbeddingsResponse(
            root=vector_array.embedding_vector
        )
    else:
        # 超过了原本可以嵌入的最大文本数组长度，那么会走接下来这一步，然后也会展示进度条
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
        results = []
        for future in tqdm_asyncio(
            asyncio.as_completed(tasks), total=len(tasks), desc="批量生成文本分块的向量"
        ):
            result = await future
            # 如果结果是列表，直接扩展结果列表，而不是追加
            results.append(result)
        final_result = [
            item for sub_list in results for item in sub_list.embedding_vector
        ]
        total_embedding_tokens_usage = sum([item.cost_tokens for item in results])
        embedding_token_usage_var.set(total_embedding_tokens_usage)

        return BatchTextChunkGenerateEmbeddingsResponse(root=final_result)


# # 编写测试代码, 测试成功
# import asyncio


# async def main():
#     await batch_text_chunk_generate_embeddings_process(
#         [
#             "你好",
#             "我是",
#             "一个",
#             "你好",
#             "我是",
#             "一个",
#             "你好",
#             "我是",
#             "一个",
#             "你好",
#             "我是",
#         ]
#     )

#     print(embedding_token_usage_var.get())


# asyncio.run(main())
