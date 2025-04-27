# context_holder.py
from contextvars import ContextVar

# 现在开始写全局上下文
llm_token_usage_var: ContextVar[int] = ContextVar("llm_token_usage", default=0)
embedding_token_usage_var: ContextVar[int] = ContextVar(
    "embedding_token_usage", default=0
)
