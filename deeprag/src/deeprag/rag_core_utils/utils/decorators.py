from functools import wraps
from deeprag.rag_core_utils.utils.context_holder import (
    llm_token_usage_var,
    embedding_token_usage_var,
)
from loguru import logger
import traceback


def llm_record_token_usage(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        if hasattr(result, "cost_tokens"):
            try:
                llm_token_usage_var.set(result.cost_tokens)
            except Exception as e:
                print(e)
                print(traceback.format_exc())
        return result

    return wrapper


def embedding_record_token_usage(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        if hasattr(result, "cost_tokens"):
            try:
                embedding_token_usage_var.set(result.cost_tokens)
            except Exception as e:
                print(e)
                print(traceback.format_exc())
        return result

    return wrapper
