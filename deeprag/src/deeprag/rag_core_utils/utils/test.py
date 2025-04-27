from deeprag.rag_core_utils.utils.decorators import (
    embedding_record_token_usage,
    embedding_token_usage_var,
)
import asyncio
from deeprag.workflow.data_model import EmbeddingResponseWithCostTokens


@embedding_record_token_usage
async def test():
    return EmbeddingResponseWithCostTokens(embedding_vector=[[1, 2]], cost_tokens=3)


@embedding_record_token_usage
async def do_work():
    return EmbeddingResponseWithCostTokens(embedding_vector=[[1, 2]], cost_tokens=4)


async def main():
    await test()
    total_token = embedding_token_usage_var.get()
    print(total_token)
    await do_work()
    total_token += embedding_token_usage_var.get()
    print(total_token)


asyncio.run(main())
