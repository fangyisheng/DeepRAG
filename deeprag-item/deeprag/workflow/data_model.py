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
    text: str
    type: str


class EntityIdInt(BaseEntity):
    id: int


class EntityIdStr(BaseEntity):
    id: str


class Relations(BaseModel):
    head: str
    tail: str
    type: str
    description: str


class FirstExtractedGraphData(BaseModel):
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
            {
                "entities": [
                    {"id": 0, "text": "深度求索", "type": "公司"},
                    {"id": 1, "text": "DeepSeek", "type": "公司"},
                    {"id": 2, "text": "全球 AI 领域", "type": "领域"},
                    {"id": 3, "text": "2023 年", "type": "时间"},
                    {"id": 4, "text": "美股市场", "type": "市场"},
                    {"id": 5, "text": "1 月 27 日", "type": "时间"},
                    {"id": 6, "text": "英伟达", "type": "公司"},
                    {"id": 7, "text": "美国股市", "type": "市场"},
                ],
                "relations": [
                    {
                        "head": 1,
                        "tail": 2,
                        "type": "在领域中崭露头角",
                        "description": "DeepSeek 在全球 AI 领域成为众人瞩目的焦点。",
                    },
                    {
                        "head": 1,
                        "tail": 3,
                        "type": "成立于时间",
                        "description": "深度求索（DeepSeek）成立于 2023 年。",
                    },
                    {
                        "head": 1,
                        "tail": 4,
                        "type": "对市场产生影响",
                        "description": "深度求索的崛起对美股市场产生了明显影响。",
                    },
                    {
                        "head": 5,
                        "tail": 6,
                        "type": "股价大跌时间",
                        "description": "1 月 27 日，英伟达收盘大跌超过 17%。",
                    },
                    {
                        "head": 6,
                        "tail": 7,
                        "type": "创下市场记录",
                        "description": "英伟达单日市值蒸发 5890 亿美元，创下美国股市历史上最高纪录。",
                    },
                    {
                        "head": 1,
                        "tail": 6,
                        "type": "被认为是重要因素",
                        "description": "DeepSeek 被认为是导致英伟达大跌的重要因素之一。",
                    },
                ],
            },
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


# class TextChunkByTokenResponse(BaseModel):
#     __root__: list[str] = Field(
#         ...,
#         description="这个数据模型是列表，列表中的每个元素是从原始长文本块根据token切分后的一个文本块",
#         examples=[
#             ["深度求索（DeepSeek）在全球 AI 领域 becomes a prominent focus.", ""],
#             ["深度求索（DeepSeek） was founded in 2023.", ""],
#             [
#                 "The rise of DeepSeek in the global AI domain has attracted attention from many people.",
#                 "",
#             ],
#         ],
#     )


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
