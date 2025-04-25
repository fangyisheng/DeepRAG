# context_holder.py
from contextvars import ContextVar

token_usage_var: ContextVar[int] = ContextVar("token_usage", default=0)
