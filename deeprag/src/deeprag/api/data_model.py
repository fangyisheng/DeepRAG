from pydantic import BaseModel
from deeprag.workflow.data_model import KnowledgeScopeLocator


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


class UploadFileRequestParam(BaseModel):
    id: str
    knowledge_space_id: str
    doc_title: str
    doc_text: str


class IndexRequestParam(BaseModel):
    collection_name: str
    knowledge_scope: KnowledgeScopeLocator
    meta_data: str | None = None
    deep_index_pattern: bool = False


class BatchIndexRequestParam(BaseModel):
    collection_name: str
    knowledge_scope: list[KnowledgeScopeLocator] | KnowledgeScopeLocator
    meta_data: str | None = None
    deep_index_pattern: bool = False


class QueryRequestParam(BaseModel):
    user_prompt: str
    knowledge_scope: KnowledgeScopeLocator
    deep_query_pattern: bool = False
    session_id: str | None = None
    context: list[RoleMessage] | None = None
    recalled_text_fragments_top_k: int = 5
