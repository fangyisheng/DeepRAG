from pydantic import BaseModel, Field, RootModel, ConfigDict
from typing import Any
from minio.helpers import ObjectWriteResult
from typing import AsyncGenerator


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

    root: list[int] = Field(
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


class CompleteGraphDataWithDescriptionEnrichment(CompleteGraphData):
    pass


class CompleteGraphDataWithCommunityIdAndDescriptionEnrichment(CompleteGraphData):
    pass


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


class BatchGenerateCommunityReportResponse(BaseModel):
    """
    community_reports_with_community_id:
    dict[str, str]
    示例数据：
    {"community_id_1": "社区检测报告的文字",
     "community_id_2": "社区检测报告的文字",
     "community_id_3": "社区检测报告的文字"}

    community_reports_structed_data_with_community_id:
    dict[str, CommunityReportStructedData]
    示例数据：
    {"community_id_1": CommunityReportStructedData(
        title="社区检测报告的标题",
        origin_description="社区检测报告的文字",
        summary="社区检测报告的摘要",
    ),
     "community_id_2": CommunityReportStructedData(
        title="社区检测报告的标题",
        origin_description="社区检测报告的文字",
     )
    }

    """

    community_reports_with_community_id: dict[str, str] = Field(
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

    community_reports_structed_data_with_community_id: dict[str, str]


class CommunityReportStructedData(BaseModel):
    title: str
    origin_description: str
    summary: str


class GenerateCommunityReportResponse(BaseModel):
    community_report: str
    community_report_structed_data: CommunityReportStructedData


# class BatchGenerateCommunityClusterResponse(BaseModel):


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
    list[FirstExtractedGraphData]
    示例数据：
    [FirstExtractedGraphData(entities=[EntityIdInt(text='深度求索', type='公司', id=0), EntityIdInt(text='DeepSeek', type='产品', id=1), EntityIdInt(text='幻方量化', type='公司', id=2), EntityIdInt(text='英伟达', type='公司', id=3), EntityIdInt(text='OpenAI', type='公司', id=4), EntityIdInt(text='GPT-4o', type='产品', id=5), EntityIdInt(text='华为云', type='产品', id=6), EntityIdInt(text='腾讯云', type='产品', id=7), EntityIdInt(text='百度云', type='产品', id=8), EntityIdInt(text='MLA', type='技术', id=9), EntityIdInt(text='MHA', type='技术', id=10), EntityIdInt(text='DeepSeek MoEs Parse', type='技术', id=11), EntityIdInt(text='CUDA', type='技术', id=12), EntityIdInt(text='PTX', type='技术', id=13), EntityIdInt(text='萤火二号', type='产品', id=14), EntityIdInt(text='A100', type='产品', id=15), EntityIdInt(text='美股', type='市场', id=16), EntityIdInt(text='2023年', type='时间', id=17), EntityIdInt(text='1月27日', type='时间', id=18), EntityIdInt(text='1月31日', type='时间', id=19), EntityIdInt(text='2月5日', type='时间', id=20), EntityIdInt(text='硅谷', type='地点', id=21)], relations=[RelationsInt(type='开发', description='深度求索开发了DeepSeek系列模型。', head=0, tail=1), RelationsInt(type='隶属', description='深度求索是从幻方量化孵化的公司。', head=0, tail=2), RelationsInt(type='影响', description='深度求索的发展对美股市场产生重大影响。', head=0, tail=16), RelationsInt(type='对比', description='DeepSeek-V3与OpenAI的GPT-4o进行性能和成本对比。', head=1, tail=5), RelationsInt(type='竞争', description='DeepSeek被认为是导致英伟达股价大跌的重要因素之一。', head=1, tail=3), RelationsInt(type='合作', description='DeepSeek模型被部署在华为云等国内云服务上。', head=1, tail=6), RelationsInt(type='合作', description='DeepSeek模型被部署在腾讯云等国内云服务上。', head=1, tail=7), RelationsInt(type='合作', description='DeepSeek模型被部署在百度云等国内云服务上。', head=1, tail=8), RelationsInt(type='采用', description='DeepSeek使用MLA架构降低内存消耗。', head=1, tail=9), RelationsInt(type='替代', description='MLA架构相较于MHA架构显著降低了内存使用率。', head=9, tail=10), RelationsInt(type='采用', description='DeepSeek通过DeepSeek MoEs Parse结构进一步优化计算成本。', head=1, tail=11), RelationsInt(type='挑战', description='DeepSeek被认为可能冲击英伟达CUDA生态的优势地位。', head=1, tail=12), RelationsInt(type='采用', description='DeepSeek在其论文中提到使用PTX语言编程以提高硬件性能。', head=1, tail=13), RelationsInt(type='开发', description='幻方量化早在2019年就开发了深度学习训练平台萤火二号。', head=2, tail=14), RelationsInt(type='搭载', description='萤火二号搭载了约1万张英伟达A100显卡。', head=14, tail=15), RelationsInt(type='成立时间', description='深度求索成立于2023年。', head=18, tail=0), RelationsInt(type='发生时间', description='1月27日美股AI、芯片股重挫。', head=19, tail=16), RelationsInt(type='上线时间', description='2月5日起，华为云等国内云厂商陆续上线DeepSeek模型。', head=20, tail=6), RelationsInt(type='认可', description='在硅谷，深度求索被称为‘来自东方的神秘力量’。', head=21, tail=0)]), FirstExtractedGraphData(entities=[EntityIdInt(text='OpenAI', type='组织', id=0), EntityIdInt(text='o1模型', type='产品', id=1), EntityIdInt(text='DeepSeek-R1模型', type='产品', id=2), EntityIdInt(text='DeepSeek', type='组织', id=3), EntityIdInt(text='周鸿祎', type='人物', id=4), EntityIdInt(text='纳米AI搜索', type='组织', id=5), EntityIdInt(text='小鹏汽车', type='组织', id=6), EntityIdInt(text='何小鹏', type='人物', id=7), EntityIdInt(text='华为', type='组织', id=8), EntityIdInt(text='阿里', type='组织', id=9), EntityIdInt(text='百度', type='组织', id=10), EntityIdInt(text='腾讯', type='组织', id=11), EntityIdInt(text='京东', type='组织', id=12)], relations=[RelationsInt(type='隶属于', description='o1模型是OpenAI开发的产品。', head=1, tail=0), RelationsInt(type='开发了', description='DeepSeek开发了DeepSeek-R1模型。', head=2, tail=3), RelationsInt(type='参与了', description='周鸿祎参与了纳米AI搜索的活动。', head=4, tail=5), RelationsInt(type='合作了', description='纳米AI搜索与DeepSeek建立了合作关系。', head=5, tail=3), RelationsInt(type='担任', description='何小鹏担任小鹏汽车的董事长。', head=7, tail=6), RelationsInt(type='接入了', description='华为接入了DeepSeek的大模型。', head=8, tail=3), RelationsInt(type='接入了', description='阿里接入了DeepSeek的大模型。', head=9, tail=3), RelationsInt(type='接入了', description='百度接入了DeepSeek的大模型。', head=10, tail=3), RelationsInt(type='接入了', description='腾讯接入了DeepSeek的大模型。', head=11, tail=3), RelationsInt(type='接入了', description='京东接入了DeepSeek的大模型。', head=12, tail=3)])]
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
    graph_data_with_enriched_description: CompleteGraphDataWithDescriptionEnrichment


class GraphDescriptionWithCommunityClusterResponse(BaseModel):
    """
    示例数据：
    graph_description_dict_by_community_id: dict[str, list] = Field(
        ...,
        description="这个数据模型是字典，键是动态的社区id,值为社区id对应的关系描述文本块的列表",
        examples=[
            {
                "community_id_1": ["关系描述文本块1", "关系描述文本块2"],
                "community_id_2": ["关系描述文本块1", "关系描述文本块2"],
            }
        ]
    )

    graph_data_with_enriched_description: (
        CompleteGraphDataWithCommunityIdAndDescriptionEnrichment
    )


    """

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
    graph_data_with_enriched_description: (
        CompleteGraphDataWithCommunityIdAndDescriptionEnrichment
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
    user_id: str | None = None
    knowledge_space_id: str | None = None
    file_id: str | None = None


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
    relation_description: str
    merged_graph_data_id: str
    community_id: str | None = None


class BatchCreateCommunityReportResponse(BaseModel):
    community_report_list: list[str]
    community_id_list: list[str]


class AssistantResponseWithCostTokens(BaseModel):
    assistant_response: str
    cost_tokens: int


class AsyncGeneratorWithCostTokens(BaseModel):
    assistant_response_generator: AsyncGenerator
    cost_tokens: int
