from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
from typing import Optional
import asyncio
from aiolimiter import AsyncLimiter
from deeprag.workflow.data_model import EmbeddingResponseWithCostTokens
from deeprag.rag_core_utils.utils.decorators import (
    embedding_record_token_usage,
)
from deeprag.rag_core_utils.utils.context_holder import (
    embedding_token_usage_var,
)

load_dotenv()
embedding_base_url = os.getenv("EMBEDDING_BASE_URL")
embedding_api_key = os.getenv("EMBEDDING_API_KEY")
embedding_model = os.getenv("EMBEDDING_MODEL")
embedding_model_max_token = int(os.getenv("EMBEDDING_MODEL_MAX_TOKEN"))
embedding_dimension = int(os.getenv("EMBEDDING_DIMENSION"))
embedding_model_rps = int(os.getenv("EMBEDDING_MODEL_RPS"))
embedding_model_tpm = int(os.getenv("EMBEDDING_MODEL_TPM"))
embedding_model_input_string_array_length = int(
    os.getenv("EMBEDDING_MODEL_INPUT_STRING_ARRAY_LENGTH")
)

max_rate = min(
    embedding_model_rps,
    embedding_model_rps
    * embedding_model_input_string_array_length
    * embedding_model_max_token
    // embedding_model_tpm,
)
# 计算得到模型每分钟的最大速率

client = AsyncOpenAI(base_url=embedding_base_url, api_key=embedding_api_key)
limiter = AsyncLimiter(max_rate=7, time_period=60)


@embedding_record_token_usage
async def text_to_vector(input: list[str], limiter=limiter):
    async with limiter:
        response = await client.embeddings.create(
            input=input, model=embedding_model, dimensions=embedding_dimension
        )
        # return [item.embedding for item in response.data]
        # print(response.usage.total_tokens)
        return EmbeddingResponseWithCostTokens(
            cost_tokens=response.usage.total_tokens,
            embedding_vector=[item.embedding for item in response.data],
        )


# # 在 main 函数中执行
# async def main():
#     await text_to_vector(["你好", "hello"])  # 调用已装饰的异步函数
#     print(f"Token usage: {embedding_token_usage_var.get()}")  # 获取 token 消耗


# asyncio.run(main())
