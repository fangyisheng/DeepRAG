from pydantic import BaseModel


class ChatRequest(BaseModel):
    """
    Chat request model.
    """

    question: str
    history: list[dict[str, str]] | None = None
    knowledge_scope: str | None = None
    recalled_text_fragments_top_k: int | None = None
    deep_query_pattern: bool | None = None
    cot_prompt: list[dict[str, str]] | None = None
    system_prompt: str | None = None


class