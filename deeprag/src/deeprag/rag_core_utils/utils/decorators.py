from functools import wraps
from deeprag.rag_core_utils.utils.context_holder import token_usage_var


def llm_record_token_usage(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        if hasattr(result, "cost_tokens"):
            try:
                token_usage_var.set(result.cost_tokens.result())
            except Exception as e:
                print(e)
        return result

    return wrapper


def embedding_record_token_usage(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        if hasattr(result, "cost_tokens"):
            try:
                token_usage_var.set(result.cost_tokens.result())
            except Exception as e:
                print(e)
        return result

    return wrapper
