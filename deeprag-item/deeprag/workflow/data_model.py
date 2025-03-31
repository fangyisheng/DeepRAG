from pydantic import BaseModel, Field, RootModel, ConfigDict
from typing import Any
from minio.helpers import ObjectWriteResult


class CompleteTextUnit(RootModel):
    """
    str
    示例数据：
    "深度求索（DeepSeek） globally becomes a prominent focus in the global AI domain."

    """

    root: str = Field(
        ...,
        description="这个数据模型是字符串，字符串是长文本块",
        examples=[
            "深度求索（DeepSeek）在全球 AI 领域 becomes a prominent focus.",
            "深度求索（DeepSeek） was founded in 2023.",
            "The rise of DeepSeek in the global AI domain has attracted attention from many people.",
        ],
    )


class TokenListByTextChunk(RootModel):
    root: list[str] = Field()


class GraphDescriptionAddCommunityWithVisualization(BaseModel):
    html_content: str
    graph_data: dict = Field(
        ...,
        description="这个数据模型是字典，和原来的graph_data相比，只不过就是在原来的graph_data的entity这个键下面的列表中的元素（字典）添加了一个键为community_id",
        examples=[],
    )


class GraphDescriptionWithVisualization(RootModel):
    root: str = Field(..., description="这个数据模型是字符串，字符串是html_content")


class ChunkedTextUnit(RootModel):
    """
    list[str]
    示例数据：
    ["深度求索（DeepSeek） globally becomes a prominent focus in the global AI domain.",
    "深度求索（DeepSeek） was founded in 2023.","The rise of DeepSeek in the global AI domain has attracted attention from many people."]
    """

    root: list[str] = Field(
        ...,
        description="这个数据模型是列表，列表中的每个元素是一个长文本块",
        examples=[
            "深度求索（DeepSeek）在全球 AI 领域 becomes a prominent focus.",
            "深度求索（DeepSeek） was founded in 2023.",
        ],
    )


class BaseEntity(BaseModel):
    """
    示例数据：
    {"text": "深度求索（DeepSeek） ",
     "type": "企业公司"}
    """

    text: str
    type: str


class EntityIdInt(BaseEntity):
    """
    示例数据：
    {"text": "深度求索（DeepSeek） ",
     "type": "企业公司",
     "id": 1}
    """

    id: int


class EntityIdStr(BaseEntity):
    """
    示例数据：
    {"text": "深度求索（DeepSeek） ",
     "type": "企业公司",
     "id": "uuid"}
    """

    id: str


class Relations(BaseModel):
    """
    示例数据：
    {"head": "深度求索（DeepSeek） ",
     "tail": " 英伟达",
     "type": "影响",
     "description": "深度求索和英伟达的关系是深度求索影响了英伟达"}
    """

    head: str
    tail: str
    type: str
    description: str


class FirstExtractedGraphData(BaseModel):
    """
    示例数据：

    """

    entities: list[EntityIdInt]
    relations: list[Relations]


class CompleteGraphData(BaseModel):
    entities: list[EntityIdStr]
    relations: list[Relations]


class BatchGenerateCommunityReportResponse(RootModel):
    """
    dict[str, list]
    示例数据：
    {"community_id_1": "社区检测报告的文字",
     "community_id_2": "社区检测报告的文字",
     "community_id_3": "社区检测报告的文字"}

    """

    root: dict[str, list] = Field(
        ...,
        description="这个数据模型是字典，键是动态的社区id,值为社区id对应的社区报告的列表",
        examples=[
            {
                "community_id_1": "社区检测报告的文字",
                "community_id_2": "社区检测报告的文字",
                "community_id_3": "社区检测报告的文字",
            },
            {
                "community_id_1": "社区检测报告的文字",
                "community_id_3": "社区检测报告的文字",
            },
        ],
    )


class BatchTextChunkGenerateEmbeddingsResponse(RootModel):
    """
    list[list]
    示例数据：
    [[0.1, 0.2, 0.3], [0.2, -0.24, 0.2]]
    """

    root: list[list] = Field(
        ...,
        description="这个数据模型是列表，列表中的每个元素是一个高维度向量的列表",
        examples=[[0.1, 0.2, 0.3], [0.2, -0.24, 0.2]],
    )


class BatchTextChunkGenerateGraphsResponse(RootModel):
    """
    list[dict]
    示例数据：
    [ {"entities": [], "relations": []},
     {"entities": [], "relations": []} ]
    """

    root: list[FirstExtractedGraphData] = Field(
        ...,
        description="这个数据模型是列表，列表中的每个元素是一个列表",
        examples=[
            {"entities": [], "relations": []},
        ],
    )


class FinalRAGAnswerStreamResponse(RootModel):
    """
    str
    示例数据：
    'data: {"answer":"", "rag_pattern":"", "workflow_id":""}'
    """

    root: str = Field(
        ...,
        description="这个数据模型是字符串，异步生成器返回一个字符串",
        examples=[
            """data: {"answer":"", "rag_pattern":"", "workflow_id":""
            }"""
        ],
    )


class FinalRAGAnswerResponse(RootModel):
    """
    str
    示例数据：
    "深度求索在全球 AI 领域 becomes a prominent focus."
    """

    root: str = Field(
        ...,
        description="这个数据模型是字符串，字符串是rag的答案",
        examples=["深度求索在全球 AI 领域 becomes a prominent focus."],
    )


class GraphDescriptionResponse(RootModel):
    """"""

    root: list[str] = Field(
        ...,
        description="这个数据模型是列表，列表中的每个元素是一个关系描述的文本字符串",
        examples=[
            "深度求索在全球 AI 领域 becomes a prominent focus.",
            "深度求索 was founded in 2023.",
            "The rise of DeepSeek in the global AI domain has attracted attention from many people.",
            "The stock price of NVIDIA dropped significantly on January 27th, 2023.",
        ],
    )


class GraphDescriptionWithCommunityClusterResponse(RootModel):
    root: dict[str, list] = Field(
        ...,
        description="这个数据模型是字典，键是动态的社区id,值为社区id对应的关系描述文本块的列表",
        examples=[
            {
                "community_id_1": ["关系描述文本块1", "关系描述文本块2"],
                "community_id_2": ["关系描述文本块1", "关系描述文本块2"],
            },
            {},
        ],
    )


class TextExtractAndCleanResponse(RootModel):
    root: str = Field(
        ...,
        description="这个数据模型是字符串，字符串是长文本块",
        examples=[
            "深度求索（DeepSeek）在全球 AI 领域 becomes a prominent focus.",
            "深度求索（DeepSeek） was founded in 2023.",
            "The rise of DeepSeek in the global AI domain has attracted attention from many people.",
        ],
    )


class DataInsertVectorDBResponse(BaseModel):
    """这边的zilliz_response需要再确认一下到底是怎么样的返回值"""

    status: str
    inserted_count: int
    collection_name: str
    zilliz_response: Any


class SearchedTextResponse(RootModel):
    root: list[str] = Field(
        ...,
        description="这个数据模型是列表，列表中的每个元素是一个字符串，字符串内容是搜索zilliz搜到的内容",
        examples=[["", "", ""], ["", "", ""]],
    )


class UploadFileToMinioResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    status: str
    object_name: ObjectWriteResult


class KnowledgeScope(BaseModel):
    user_id: str
    knowledge_space_id: str
    file_id: str
