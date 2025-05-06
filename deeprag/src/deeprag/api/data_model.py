from pydantic import BaseModel
from deeprag.workflow.data_model import KnowledgeScopeLocator
from deeprag.db.data_model import RoleMessage


class UploadFileRequestParam(BaseModel):
    id: str
    knowledge_space_id: str
    doc_title: str
    minio_bucket_name: str
    minio_object_name: str
    doc_text: str | None = None


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


class ChatRequestParam(BaseModel):
    user_prompt: str
    knowledge_scope: KnowledgeScopeLocator
    deep_query_pattern: bool = False
    session_id: str | None = None
    context: list[RoleMessage] | None = None
    recalled_text_fragments_top_k: int = 5
    stream: bool = False
