from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
from typing import Optional
import asyncio
from aiolimiter import AsyncLimiter

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


async def text_to_vector(input: list[str], limiter=limiter):
    async with limiter:
        response = await client.embeddings.create(
            input=input, model=embedding_model, dimensions=embedding_dimension
        )
        return [item.embedding for item in response.data]


# print(asyncio.run(text_to_vector(["你好", "hello"])))
