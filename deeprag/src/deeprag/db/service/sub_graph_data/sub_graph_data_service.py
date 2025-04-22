from deeprag.db.dao.sub_graph_data.sub_graph_data_dao import SubGraphDataDAO
import uuid
from deeprag.workflow.data_model import BatchTextChunkGenerateGraphsResponse
from loguru import logger


class SubGraphDataService:
    def __init__(self):
        self.dao = SubGraphDataDAO()

    async def create_sub_graph_data(
        self,
        id: str,
        text_chunk_id: str,
        graph_data: str,
        merged_graph_data_id: str,
    ):
        stored_sub_graph_data = await self.dao.create_sub_graph_data(
            id,
            text_chunk_id,
            graph_data,
            merged_graph_data_id,
        )

        return stored_sub_graph_data.model_dump()

    async def batch_create_sub_graph_data(
        self,
        text_chunk_id_list: list[str],
        sub_graph_data_list: BatchTextChunkGenerateGraphsResponse,
        merged_graph_data_id: str,
    ) -> int:
        id_list = [str(uuid.uuid4()) for _ in range(len(text_chunk_id_list))]
        sub_graph_data_list = [
            str(sub_graph_data.model_dump())
            for sub_graph_data in sub_graph_data_list.root
        ]

        stored_sub_graph_data_count = await self.dao.batch_create_sub_graph_data(
            id_list, text_chunk_id_list, sub_graph_data_list, merged_graph_data_id
        )
        return stored_sub_graph_data_count

    async def get_sub_graph_data_by_id(self, id: str):
        sub_graph_data = await self.dao.get_sub_graph_data_by_id(id)

        return sub_graph_data


# # 做个简单测试
# import asyncio
# from deeprag.workflow.data_model import (
#     FirstExtractedGraphData,
#     EntityIdInt,
#     RelationsInt,
#     BatchTextChunkGenerateGraphsResponse,
# )

# sub_graph_data_service = SubGraphDataService()
# data = asyncio.run(
#     sub_graph_data_service.batch_create_sub_graph_data(
#         [
#             "5a66a7e2-293a-4ce8-a526-58423daf3b03",
#             "c691e042-6b0b-4c49-93c5-5de0718c5d2a",
#         ],
#         BatchTextChunkGenerateGraphsResponse(
#             root=[
#                 FirstExtractedGraphData(
#                     entities=[
#                         EntityIdInt(text="深度求索", type="公司", id=0),
#                         EntityIdInt(text="DeepSeek", type="产品", id=1),
#                         EntityIdInt(text="AI", type="领域", id=2),
#                         EntityIdInt(text="英伟达", type="公司", id=3),
#                         EntityIdInt(text="幻方量化", type="公司", id=4),
#                         EntityIdInt(text="OpenAI", type="公司", id=5),
#                         EntityIdInt(text="GPT-4o", type="产品", id=6),
#                         EntityIdInt(text="MLA", type="技术", id=7),
#                         EntityIdInt(text="MHA", type="技术", id=8),
#                         EntityIdInt(text="DeepSeek MoEs Parse", type="技术", id=9),
#                         EntityIdInt(text="华为云", type="公司", id=10),
#                         EntityIdInt(text="腾讯云", type="公司", id=11),
#                         EntityIdInt(text="百度云", type="公司", id=12),
#                         EntityIdInt(text="微软", type="公司", id=13),
#                         EntityIdInt(text="亚马逊", type="公司", id=14),
#                     ],
#                     relations=[
#                         RelationsInt(
#                             type="开发",
#                             description="深度求索开发了DeepSeek系列大模型。",
#                             head=0,
#                             tail=1,
#                         ),
#                         RelationsInt(
#                             type="属于",
#                             description="DeepSeek是AI领域的新兴力量。",
#                             head=1,
#                             tail=2,
#                         ),
#                         RelationsInt(
#                             type="参与",
#                             description="英伟达参与了AI领域的硬件运算平台建设。",
#                             head=3,
#                             tail=2,
#                         ),
#                         RelationsInt(
#                             type="出身于",
#                             description="深度求索出身于幻方量化公司。",
#                             head=0,
#                             tail=4,
#                         ),
#                         RelationsInt(
#                             type="开发",
#                             description="OpenAI开发了GPT-4o模型。",
#                             head=5,
#                             tail=6,
#                         ),
#                         RelationsInt(
#                             type="改进",
#                             description="MLA架构改进了传统的MHA架构，降低了内存使用。",
#                             head=7,
#                             tail=8,
#                         ),
#                         RelationsInt(
#                             type="优化",
#                             description="DeepSeek MoEs Parse结构优化了DeepSeek模型的计算成本。",
#                             head=9,
#                             tail=1,
#                         ),
#                         RelationsInt(
#                             type="上线",
#                             description="华为云上线了DeepSeek模型。",
#                             head=10,
#                             tail=1,
#                         ),
#                         RelationsInt(
#                             type="上线",
#                             description="腾讯云上线了DeepSeek模型。",
#                             head=11,
#                             tail=1,
#                         ),
#                         RelationsInt(
#                             type="上线",
#                             description="百度云上线了DeepSeek模型。",
#                             head=12,
#                             tail=1,
#                         ),
#                         RelationsInt(
#                             type="接入",
#                             description="微软接入了DeepSeek模型。",
#                             head=13,
#                             tail=1,
#                         ),
#                         RelationsInt(
#                             type="接入",
#                             description="亚马逊接入了DeepSeek模型。",
#                             head=14,
#                             tail=1,
#                         ),
#                     ],
#                 ),
#                 FirstExtractedGraphData(
#                     entities=[
#                         EntityIdInt(text="OpenAI", type="公司", id=0),
#                         EntityIdInt(text="o1模型", type="产品", id=1),
#                         EntityIdInt(text="DeepSeek-R1模型", type="产品", id=2),
#                         EntityIdInt(text="DeepSeek", type="公司", id=3),
#                         EntityIdInt(text="周鸿祎", type="人物", id=4),
#                         EntityIdInt(text="纳米AI搜索", type="公司", id=5),
#                         EntityIdInt(text="小鹏汽车", type="公司", id=6),
#                         EntityIdInt(text="何小鹏", type="人物", id=7),
#                         EntityIdInt(text="华为", type="公司", id=8),
#                         EntityIdInt(text="阿里", type="公司", id=9),
#                         EntityIdInt(text="百度", type="公司", id=10),
#                         EntityIdInt(text="腾讯", type="公司", id=11),
#                         EntityIdInt(text="京东", type="公司", id=12),
#                     ],
#                     relations=[
#                         RelationsInt(
#                             type="开发",
#                             description="OpenAI 开发了 o1 模型，但该模型不开源且收费高。",
#                             head=0,
#                             tail=1,
#                         ),
#                         RelationsInt(
#                             type="开发",
#                             description="DeepSeek 开发了 DeepSeek-R1 模型，并免费让用户使用。",
#                             head=3,
#                             tail=2,
#                         ),
#                         RelationsInt(
#                             type="合作",
#                             description="纳米 AI 搜索与 DeepSeek 建立联系并接入和本地化部署其大模型。",
#                             head=5,
#                             tail=3,
#                         ),
#                         RelationsInt(
#                             type="参与",
#                             description="周鸿祎在纳米 AI 搜索的活动中提到与 DeepSeek 的合作。",
#                             head=4,
#                             tail=5,
#                         ),
#                         RelationsInt(
#                             type="计划接入",
#                             description="小鹏汽车董事长何小鹏表示可以期待小鹏汽车接入 DeepSeek 大模型。",
#                             head=6,
#                             tail=3,
#                         ),
#                         RelationsInt(
#                             type="担任",
#                             description="何小鹏是小鹏汽车的董事长。",
#                             head=7,
#                             tail=6,
#                         ),
#                         RelationsInt(
#                             type="合作",
#                             description="华为宣布接入 DeepSeek 大模型。",
#                             head=8,
#                             tail=3,
#                         ),
#                         RelationsInt(
#                             type="合作",
#                             description="阿里宣布接入 DeepSeek 大模型。",
#                             head=9,
#                             tail=3,
#                         ),
#                         RelationsInt(
#                             type="合作",
#                             description="百度宣布接入 DeepSeek 大模型。",
#                             head=10,
#                             tail=3,
#                         ),
#                         RelationsInt(
#                             type="合作",
#                             description="腾讯宣布接入 DeepSeek 大模型。",
#                             head=11,
#                             tail=3,
#                         ),
#                         RelationsInt(
#                             type="合作",
#                             description="京东宣布接入 DeepSeek 大模型。",
#                             head=12,
#                             tail=3,
#                         ),
#                     ],
#                 ),
#             ]
#         ),
#         ["uuid_1", "uuid_2"],
#     )
# )
# print(data)
