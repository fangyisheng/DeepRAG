from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
from typing import Optional, AsyncGenerator
import asyncio
from loguru import logger
from deeprag.workflow.data_model import (
    AssistantResponseWithCostTokens,
    AsyncGeneratorWithCostTokens,
)
from deeprag.rag_core_utils.utils.decorators import (
    llm_record_token_usage,
)
from deeprag.rag_core_utils.utils.context_holder import (
    llm_token_usage_var,
)

load_dotenv()
llm_base_url = os.getenv("LLM_BASE_URL")
llm_api_key = os.getenv("LLM_API_KEY")
llm_model = os.getenv("LLM_MODEL")

client = AsyncOpenAI(base_url=llm_base_url, api_key=llm_api_key)


async def llm_chat(
    system_prompt: str,
    user_prompt: str,
    context_histroy: list[dict[str, str]] | None = None,
) -> AsyncGeneratorWithCostTokens:
    if context_histroy is None:
        context_histroy = []
    chat_completion = await client.chat.completions.create(
        model=llm_model,
        messages=[{"role": "system", "content": system_prompt}]
        + context_histroy
        + [{"role": "user", "content": user_prompt}],
        stream=True,
        stream_options={"include_usage": True},
    )
    cost_tokens = asyncio.Future()

    async def generator() -> AsyncGenerator[str, None]:
        async for chunk in chat_completion:
            if chunk.choices:
                yield chunk.choices[0].delta.content
            if chunk.usage:
                cost_tokens.set_result(chunk.usage.total_tokens)

    return AsyncGeneratorWithCostTokens(
        assistant_response_generator=generator(), cost_tokens=cost_tokens
    )


@llm_record_token_usage
async def llm_chat_not_stream(
    system_prompt: str,
    user_prompt: str,
    context_histroy: list[dict[str, str]] | None = None,
) -> AssistantResponseWithCostTokens:
    if context_histroy is None:
        context_histroy = []
    chat_completion = await client.chat.completions.create(
        model=llm_model,
        messages=[{"role": "system", "content": system_prompt}]
        + context_histroy
        + [{"role": "user", "content": user_prompt}],
        stream=False,
    )
    return AssistantResponseWithCostTokens(
        assistant_response=chat_completion.choices[0].message.content,
        cost_tokens=chat_completion.usage.total_tokens,
    )


@llm_record_token_usage
async def llm_service(
    system_prompt: str,
    user_prompt: str | None = None,
    context_histroy: list[dict[str, str]] | None = None,
    cot_prompt: list[dict[str, str]] | None = None,
) -> AssistantResponseWithCostTokens:
    if context_histroy is None:
        context_histroy = []
    if cot_prompt is None:
        cot_prompt = []
    if user_prompt is None:
        chat_completion = await client.chat.completions.create(
            model=llm_model,
            messages=[{"role": "system", "content": system_prompt}]
            + context_histroy
            + cot_prompt,
            stream=False,
        )
    else:
        chat_completion = await client.chat.completions.create(
            model=llm_model,
            messages=[{"role": "system", "content": system_prompt}]
            + context_histroy
            + [{"role": "user", "content": user_prompt}]
            + cot_prompt,
            stream=False,
        )

    return AssistantResponseWithCostTokens(
        assistant_response=chat_completion.choices[0].message.content,
        cost_tokens=chat_completion.usage.total_tokens,
    )


async def llm_service_stream(
    system_prompt: str,
    user_prompt: str,
    context_histroy: list[dict[str, str]] | None = None,
    cot_prompt: list[dict[str, str]] | None = None,
) -> AsyncGeneratorWithCostTokens:
    if context_histroy is None:
        context_histroy = []
    if cot_prompt is None:
        cot_prompt = []

    chat_completion = await client.chat.completions.create(
        model=llm_model,
        messages=[{"role": "system", "content": system_prompt}]
        + context_histroy
        + [{"role": "user", "content": user_prompt}],
        stream=True,
        stream_options={"include_usage": True},
    )
    cost_tokens = asyncio.Future()

    async def generator() -> AsyncGenerator[str, None]:
        async for chunk in chat_completion:
            if chunk.choices:
                yield chunk.choices[0].delta.content
            if chunk.usage:
                cost_tokens.set_result(chunk.usage.total_tokens)

    return AsyncGeneratorWithCostTokens(
        assistant_response_generator=generator(), cost_tokens=cost_tokens
    )


# # test code 测试通过
# async def main():
#     chat = await llm_chat(
#         system_prompt="你是一个强大的人工智能助手", user_prompt="你好？"
#     )
#     async for response in chat.assistant_response_generator:
#         print(response)
#         print("\n\n")
#     print(chat.cost_tokens.result())


# # main函数没有输出，所以打印它的结果，结果是None
# # if __name__ == "__main__":
# #     print(asyncio.run(main()))
# asyncio.run(main())


# # test code 测试通过
# async def main():
#     chat = await llm_service(system_prompt="你是一个强大的人工智能助手")
#     print(chat.assistant_response)
#     print(chat.cost_tokens)
#     # print(chat)


# # main函数没有输出，所以打印它的结果，结果是None
# # if __name__ == "__main__":
# #     print(asyncio.run(main()))
# asyncio.run(main())
