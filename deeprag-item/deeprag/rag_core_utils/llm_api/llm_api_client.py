from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
from typing import Optional, AsyncGenerator
import asyncio
from loguru import logger

load_dotenv()
llm_base_url = os.getenv("LLM_BASE_URL")
llm_api_key = os.getenv("LLM_API_KEY")
llm_model = os.getenv("LLM_MODEL")

client = AsyncOpenAI(base_url=llm_base_url, api_key=llm_api_key)


async def llm_chat(
    system_prompt: Optional[str] = "",
    context_histroy: Optional[list] = [],
    user_prompt: Optional[str] = "",
) -> AsyncGenerator[str, None]:
    chat_completion = await client.chat.completions.create(
        model=llm_model,
        messages=[{"role": "system", "content": system_prompt}]
        + context_histroy
        + [{"role": "user", "content": user_prompt}],
        stream=True,
    )
    async for chunk in chat_completion:
        yield chunk.choices[0].delta.content


async def llm_chat_not_stream(
    system_prompt: Optional[str] = "",
    context_histroy: Optional[list] = [],
    user_prompt: Optional[str] = "",
) -> str:
    chat_completion = await client.chat.completions.create(
        model=llm_model,
        messages=[{"role": "system", "content": system_prompt}]
        + context_histroy
        + [{"role": "user", "content": user_prompt}],
        stream=False,
    )
    return chat_completion.choices[0].message.content


async def llm_service(
    system_prompt: Optional[str] = "",
    context_histroy: Optional[list] = [],
    user_prompt: Optional[str] = "",
    cot_prompt: Optional[str] = [],
) -> str:
    chat_completion = await client.chat.completions.create(
        model=llm_model,
        messages=[{"role": "system", "content": system_prompt}]
        + context_histroy
        + [{"role": "user", "content": user_prompt}]
        + cot_prompt,
        stream=False,
    )
    return chat_completion.choices[0].message.content


async def llm_service_stream(
    system_prompt: Optional[str] = "",
    context_histroy: Optional[list] = [],
    user_prompt: Optional[str] = "",
    cot_prompt: Optional[str] = [],
):
    chat_completion = await client.chat.completions.create(
        model=llm_model,
        messages=[{"role": "system", "content": system_prompt}]
        + context_histroy
        + [{"role": "user", "content": user_prompt}],
        stream=True,
    )
    logger.info(
        f"大模型的输入：{
            [{'role': 'system', 'content': system_prompt}]
            + context_histroy
            + [{'role': 'user', 'content': user_prompt}]
            + cot_prompt
        }"
    )
    async for chunk in chat_completion:
        yield chunk.choices[0].delta.content


# test code
# async def main():
#     async for item in llm_chat(system_prompt="你是一个强大的人工智能助手", user_prompt="你好？", stream=True):
#         print(item, end="", flush=True)  # 实时打印
#     print() # 换行

# if __name__ == "__main__":
#     asyncio.run(main())
