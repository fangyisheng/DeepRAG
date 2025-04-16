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
    """
    list[int]
    示例数据：
    [123,123,123,124]
    """

    root: list[str] = Field(
        ...,
        description="这个数据模型是列表，列表中的每个元素是对应的文本块消耗的Token数量",
        examples=[[123, 123, 123, 124], [89, 89, 89, 89]],
    )


class GraphDataWithVisualization(RootModel):
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
    type: str | list[str]


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


class EntityIdStrWithCommunityId(EntityIdStr):
    community_id: str


class BaseRelations(BaseModel):
    """
    示例数据：
    {"head": "深度求索（DeepSeek） ",
     "tail": " 英伟达",
     "type": "影响",
     "description": "深度求索和英伟达的关系是深度求索影响了英伟达"}
    """

    type: str | list[str]
    description: str


class RelationsInt(BaseRelations):
    head: int
    tail: int


class RelationsStr(BaseRelations):
    id: str
    head: str
    tail: str


class RelationsStrWithCommunityId(RelationsStr):
    community_id: str


class FirstExtractedGraphData(BaseModel):
    """
    示例数据：
    {
        "entities": [
            {"id": 0, "text": "深度求索（DeepSeek）", "type": "组织"},
            {"id": 1, "text": "全球 AI 领域", "type": "领域"},
            {"id": 2, "text": "2023 年", "type": "时间"},
            {"id": 3, "text": "美股市场", "type": "地点"},
            {"id": 4, "text": "1 月 27 日", "type": "时间"},
            {"id": 5, "text": "美股 AI、芯片股", "type": "股票"},
            {"id": 6, "text": "英伟达", "type": "组织"},
            {"id": 7, "text": "美国股市", "type": "地点"},
        ],
        "relations": [
            {
                "head": 0,
                "tail": 1,
                "type": "在领域中崭露头角",
                "description": "深度求索（DeepSeek）在全球 AI 领域成为众人瞩目的焦点。",
            },
            {
                "head": 0,
                "tail": 2,
                "type": "成立于",
                "description": "深度求索（DeepSeek）成立于2023年。",
            },
            {
                "head": 0,
                "tail": 3,
                "type": "影响力体现在",
                "description": "深度求索（DeepSeek）的影响力在美股市场有明显体现。",
            },
            {
                "head": 4,
                "tail": 5,
                "type": "导致重挫",
                "description": "1月27日，美股AI、芯片股重挫。",
            },
            {
                "head": 5,
                "tail": 6,
                "type": "影响公司股价",
                "description": "英伟达收盘大跌超过17%，单日市值蒸发5890亿美元。",
            },
            {
                "head": 6,
                "tail": 7,
                "type": "创历史纪录",
                "description": "创下美国股市历史上最高纪录。",
            },
            {
                "head": 0,
                "tail": 5,
                "type": "被认为是重要因素",
                "description": "深度求索（DeepSeek）被认为是美股AI、芯片股波动的重要因素之一。",
            },
        ],
    }

    """

    entities: list[EntityIdInt]
    relations: list[RelationsInt]


class CompleteGraphData(BaseModel):
    """
    示例数据的__dict__：
    {
        "entities": [
            EntityIdStr(
                text="深度求索（DeepSeek）",
                type="组织",
                id="7814ff17-a116-4d1e-af36-6cb63fdf116c",
            ),
            EntityIdStr(
                text="全球 AI 领域", type="领域", id="3839eb8e-73af-4b24-96da-9c2197b7a1aa"
            ),
            EntityIdStr(
                text="2023 年", type="时间", id="1fc58fb7-c56c-4037-8752-47b2d618deb5"
            ),
            EntityIdStr(
                text="美股市场", type="地点", id="5613dd34-ba51-46fb-9e93-582253828dfd"
            ),
            EntityIdStr(
                text="1 月 27 日", type="时间", id="40c60a69-7dda-4302-9d0f-e1bd1fc88784"
            ),
            EntityIdStr(
                text="美股 AI、芯片股",
                type="股票",
                id="5202c246-bd22-460a-ae8a-d649e822c832",
            ),
            EntityIdStr(
                text="英伟达", type="组织", id="b18fe663-db36-48ea-a8f9-4760d23682c9"
            ),
            EntityIdStr(
                text="美国股市", type="地点", id="671c921d-c047-44b7-8b2d-7379702a80c7"
            ),
        ],
        "relations": [
            Relations(
                head="7814ff17-a116-4d1e-af36-6cb63fdf116c",
                tail="3839eb8e-73af-4b24-96da-9c2197b7a1aa",
                type="在领域中崭露头角",
                description="深度求索（DeepSeek）在全球 AI 领域成为众人瞩目的焦点。",
                id=""
            ),
            Relations(
                head="7814ff17-a116-4d1e-af36-6cb63fdf116c",
                tail="1fc58fb7-c56c-4037-8752-47b2d618deb5",
                type="成立于",
                description="深度求索（DeepSeek）成立于2023年。",
                id=""
            ),
            Relations(
                head="7814ff17-a116-4d1e-af36-6cb63fdf116c",
                tail="5613dd34-ba51-46fb-9e93-582253828dfd",
                type="影响力体现在",
                description="深度求索（DeepSeek）的影响力在美股市场有明显体现。",
                id = ""
            ),
            Relations(
                head="40c60a69-7dda-4302-9d0f-e1bd1fc88784",
                tail="5202c246-bd22-460a-ae8a-d649e822c832",
                type="导致重挫",
                description="1月27日，美股AI、芯片股重挫。",
                id = ""
            ),
            Relations(
                head="5202c246-bd22-460a-ae8a-d649e822c832",
                tail="b18fe663-db36-48ea-a8f9-4760d23682c9",
                type="影响公司股价",
                description="英伟达收盘大跌超过17%，单日市值蒸发5890亿美元。",
                id = ""
            ),
            Relations(
                head="b18fe663-db36-48ea-a8f9-4760d23682c9",
                tail="671c921d-c047-44b7-8b2d-7379702a80c7",
                type="创历史纪录",
                description="创下美国股市历史上最高纪录。",
                id = ""
            ),
            Relations(
                head="7814ff17-a116-4d1e-af36-6cb63fdf116c",
                tail="5202c246-bd22-460a-ae8a-d649e822c832",
                type="被认为是重要因素",
                description="深度求索（DeepSeek）被认为是美股AI、芯片股波动的重要因素之一。",
                id = ""
            ),
        ],
    }
    """

    entities: list[EntityIdStr]
    relations: list[RelationsStr]


class CompleteGraphDataWithCommunityId(BaseModel):
    entities: list[EntityIdStrWithCommunityId]
    relations: list[RelationsStrWithCommunityId]


class GraphDataAddCommunityWithVisualization(BaseModel):
    """
    示例数据：
    html_content:str 是一对html和css和js的代码字符串，放在浏览器里可以可视化知识图谱

    graph_data:dict 在原来的graph_data的entity这个键下面的列表中的元素（字典）添加了一个键为community_id


    """

    html_content: str
    graph_data: CompleteGraphDataWithCommunityId = Field(
        ...,
        description="这个数据模型是字典，和原来的graph_data相比，只不过就是在原来的graph_data的entity这个键下面的列表中的元素（字典）添加了一个键为community_id",
        examples=[],
    )


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


class GraphDescriptionResponse(BaseModel):
    """
    graph_description_list: list[str]
    示例数据：
    ["深度求索和英伟达之间的关系是xxxx","xxxx和xxxx的关系是xxxxxxx"]

    graph_data_with_enriched_description: CompleteGraphData
    示例数据：


    """

    graph_description_list: list[str] = Field(
        ...,
        description="这个数据模型是列表，列表中的每个元素是一个关系描述的文本字符串",
        examples=[
            "深度求索在全球 AI 领域 becomes a prominent focus.",
            "深度求索 was founded in 2023.",
            "The rise of DeepSeek in the global AI domain has attracted attention from many people.",
            "The stock price of NVIDIA dropped significantly on January 27th, 2023.",
        ],
    )
    graph_data_with_enriched_description: CompleteGraphData


class GraphDescriptionWithCommunityClusterResponse(BaseModel):
    graph_description_dict_by_community_id: dict[str, list] = Field(
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
    graph_data_with_enriched_description: CompleteGraphDataWithCommunityId


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
    minio_upload_result: ObjectWriteResult


class User(BaseModel):
    user_id: str
    user_name: str


class KnowledgeSpace(BaseModel):
    knowledge_space_id: str
    knowledge_space_name: str


class File(BaseModel):
    file_id: str
    file_name: str


class KnowledgeScope(BaseModel):
    user: User
    knowledge_space: KnowledgeSpace
    file: File


class KnowledgeScopeRealName(BaseModel):
    user_name: str
    knowledge_space_name: str
    file_name: str


class KnowledgeScopeLocator(BaseModel):
    user_id: str
    knowledge_space_id: str
    file_id: str


class MinioObjectReference(BaseModel):
    bucket_name: str
    object_name: str


class KnowledgeScopeMinioMapping(BaseModel):
    knowledge_scope: KnowledgeScopeLocator
    minio_object_reference: MinioObjectReference


class SystemPrompt(RootModel):
    """
        系统提示词
        str
        示例数据：
        "#### **Task（任务）**
    详细描述需要完成的任务或目标。
    例如：
    - "分析以下数据集，并总结出关键趋势。"
    - "根据提供的背景信息，撰写一篇500字的文章。"
    - "编写一个Python函数，实现特定的功能。"

    #### **Format（格式）**
    说明输出的具体格式或结构要求。
    例如：
    - "请以Markdown格式输出结果。"
    - "答案需包含标题、正文和结论三部分。"
    - "代码需符合PEP 8规范，并添加必要的注释。"

    #### **Warnings（注意事项）**
    列出需要特别注意的事项或避免的错误。
    例如：
    - "避免使用过于复杂的术语，确保内容通俗易懂。"
    - "不要遗漏任何关键步骤，确保逻辑完整。"
    - "确保代码经过测试，无语法错误或运行异常。"

    #### **Background（背景信息）**
    提供任务相关的背景或上下文信息，帮助接收者更好地理解任务需求。
    例如：
    - "该数据集来源于某电商平台的用户行为记录，时间跨度为一年。"
    - "这篇文章的目标读者是初学者，因此需要从基础概念讲起。"
    - "此功能将用于一个实时推荐系统，性能优化至关重要。""
    """

    root: str = Field(
        ...,
        description="这个数据模型是字符串，字符串是系统提示",
        examples=[
            "You are a helpful assistant.",
            "You are a helpful assistant.",
        ],
    )


class FlattenEntityRelation(BaseModel):
    """
    示例数据：

    """

    id: str
    head_entity: str
    tail_entity: str
    relation: str
    merged_graph_data_id: str
    commuity_id: str | None = None
