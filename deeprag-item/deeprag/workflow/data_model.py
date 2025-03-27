from pydantic import BaseModel, Field
from typing import AsyncGenerator


class BatchGenerateCommunityReport(BaseModel):
    coummunity_reports: dict[str, list] = Field(
        ...,
        description="这个数据模型是字典，键是动态的社区id,值为社区id对应的社区报告的列表",
        examples=[
            {
                "community_id_1": ["关系描述文本块1", "关系描述文本块2"],
                "community_id_2": ["关系描述文本块1", "关系描述文本块2"],
                "community_id_3": ["关系描述文本块1", "关系描述文本块2"],
            }
        ],
    )


class BatchTextChunkGenerateEmbeddings(BaseModel):
    __root__: list[list] = Field(
        ...,
        description="这个数据模型是列表，列表中的每个元素是一个高维度向量的列表",
        examples=[[0.1, 0.2, 0.3], [0.2, -0.24, 0.2]],
    )


class BatchTextChunkGenerateGraphs(BaseModel):
    __root__: list[dict] = Field(
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


class FinalRAGAnswerStream(BaseModel):
    __root__: AsyncGenerator[str, None] = Field(
        ..., description="这个数据模型是异步生成器，异步生成器返回一个字符串"
    )


class FinalRAGAnswer(BaseModel):
    __root__: str = Field(..., description="这个数据模型是字符串，字符串是rag的答案")


class GraphDescription(BaseModel):
    __root__: list[str] = Field(
        ...,
        description="这个数据模型是列表，列表中的每个元素是一个关系描述的文本字符串",
        examples=[
            "深度求索在全球 AI 领域 becomes a prominent focus.",
            "深度求索 was founded in 2023.",
            "The rise of DeepSeek in the global AI domain has attracted attention from many people.",
            "The stock price of NVIDIA dropped significantly on January 27th, 2023.",
        ],
    )


class GraphDescriptionWithCommunityCluster(BaseModel):
    __root__: dict[str, list] = Field(
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


class TextChunkByToken(BaseModel):
    __root__: list[str] = Field(
        ...,
        description="这个数据模型是列表，列表中的每个元素是从原始长文本块根据token切分后的一个文本块",
        examples=[
            ["深度求索（DeepSeek）在全球 AI 领域 becomes a prominent focus.", ""],
            ["深度求索（DeepSeek） was founded in 2023.", ""],
            [
                "The rise of DeepSeek in the global AI domain has attracted attention from many people.",
                "",
            ],
        ],
    )


class TextExtractAndClean(BaseModel):
    __root__: str = Field(
        ...,
        description="这个数据模型是字符串，字符串是长文本块",
        examples=[
            "深度求索（DeepSeek）在全球 AI 领域 becomes a prominent focus.",
            "深度求索（DeepSeek） was founded in 2023.",
            "The rise of DeepSeek in the global AI domain has attracted attention from many people.",
        ],
    )


class VectorWithTextToVectorDB(BaseModel):
    __root__: list[dict] = Field(
        ...,
        description="这个数据模型是列表，列表中的每个元素是一个字典，字典的键是id,value是向量",
        examples=[
            {
                "id": 0,
                "vector": [0.1, 0.2, 0.3],
            },
            {"id": 1, "vector": [0.2, -0.24, 0.2]},
        ],
    )
