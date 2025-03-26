from pydantic import BaseModel

"""并不会在输入数据的时候进行强制的数据验证，只会静态地提醒你要输入什么结构的数据"""


class CommunityCluster(BaseModel):
    id: str
    community: str
    community_title: str


class CommunityReport(BaseModel):
    id: str
    community_report: str
    community_id: str


class File(BaseModel):
    id: str
    knowledge_space_id: str
    doc_title: str
    doc_text: str


"""感觉这个类还需要打磨一下，增加数据验证啥的?? 明天再思考一下"""


class UpdatedFile(BaseModel):
    doc_title: str | None = None
    doc_text: str | None = None


class FlattenEntityRelation(BaseModel):
    id: str
    head_entity: str
    tail_entity: str
    relation: str
    merged_graph_data_id: str
    commuity_id: str


class KnowledgeSpace(BaseModel):
    id: str
    user_id: str
    knowledge_space_title: str


class UpdateKnowledgeSpace(BaseModel):
    knowledge_space_title: str


class LLMChat(BaseModel):
    id: str
    user_id: str
    user_prompt: str
    user_context: str
    llm_answer: str
    message_start_time: str
    message_end_time: str
    message_duration_time: str
    session_id: str
    cost_tokens: str


class MergedGraphData(BaseModel):
    id: str
    sub_graph_data_id: str
    merged_graph_data: str
    merged_graph_data_visualization_html: str


class RAGParam(BaseModel):
    id: str
    grounds_for_response: str
    message_id: str


class SubGraphData(BaseModel):
    id: str
    text_chunk_id: str
    sub_graph_data: str
    merged_graph_data_id: str


class TextChunk(BaseModel):
    id: str
    doc_id: str
    text_chunk: str
    n_tokens: str


class User(BaseModel):
    id: str
    user_name: str


class WorkFlow(BaseModel):
    id: str
    status: str
    action: str
    workflow_start_time: str
    workflow_end_time: str
    workflow_duration_time: str
