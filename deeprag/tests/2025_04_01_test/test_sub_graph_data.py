from deeprag.db.dao.sub_graph_data.sub_graph_data_dao import SubGraphDataDAO
from deeprag.db.service.sub_graph_data.sub_graph_data_service import (
    SubGraphDataService,
)
from deeprag.workflow.data_model import BatchTextChunkGenerateGraphsResponse
from deeprag.workflow.batch_text_chunk_generate_graphs import (
    batch_text_chunk_generate_graphs_process,
)
from deeprag.workflow.data_model import (
    FirstExtractedGraphData,
    EntityIdInt,
    RelationsInt,
)

data = BatchTextChunkGenerateGraphsResponse(
    root=[
        FirstExtractedGraphData(
            entities=[
                EntityIdInt(text="深度求索", type="公司", id=0),
                EntityIdInt(text="DeepSeek", type="产品", id=1),
                EntityIdInt(text="英伟达", type="公司", id=2),
                EntityIdInt(text="幻方量化", type="公司", id=3),
                EntityIdInt(text="OpenAI", type="公司", id=4),
                EntityIdInt(text="GPT-4o", type="产品", id=5),
                EntityIdInt(text="CUDA", type="技术", id=6),
                EntityIdInt(text="华为云", type="公司", id=7),
                EntityIdInt(text="腾讯云", type="公司", id=8),
                EntityIdInt(text="百度云", type="公司", id=9),
                EntityIdInt(text="MLA", type="技术", id=10),
                EntityIdInt(text="MHA", type="技术", id=11),
                EntityIdInt(text="DeepSeek MoEs Parse", type="技术", id=12),
                EntityIdInt(text="微软", type="公司", id=13),
                EntityIdInt(text="亚马逊", type="公司", id=14),
            ],
            relations=[
                RelationsInt(
                    type="开发",
                    description="深度求索开发了DeepSeek系列模型。",
                    head=0,
                    tail=1,
                ),
                RelationsInt(
                    type="影响",
                    description="英伟达在美股市场的股价波动被认为与DeepSeek的崛起有关。",
                    head=2,
                    tail=1,
                ),
                RelationsInt(
                    type="孵化",
                    description="幻方量化孵化了深度求索这家公司。",
                    head=3,
                    tail=0,
                ),
                RelationsInt(
                    type="开发", description="OpenAI开发了GPT-4o模型。", head=4, tail=5
                ),
                RelationsInt(
                    type="拥有",
                    description="英伟达拥有CUDA运算平台技术。",
                    head=2,
                    tail=6,
                ),
                RelationsInt(
                    type="合作",
                    description="华为云与DeepSeek展开合作，上线其模型。",
                    head=7,
                    tail=1,
                ),
                RelationsInt(
                    type="合作",
                    description="腾讯云与DeepSeek展开合作，上线其模型。",
                    head=8,
                    tail=1,
                ),
                RelationsInt(
                    type="合作",
                    description="百度云与DeepSeek展开合作，上线其模型。",
                    head=9,
                    tail=1,
                ),
                RelationsInt(
                    type="提出",
                    description="深度求索提出了MLA多头潜在注意力机制技术。",
                    head=0,
                    tail=10,
                ),
                RelationsInt(
                    type="改进",
                    description="MLA技术相比MHA架构显著降低了内存使用。",
                    head=10,
                    tail=11,
                ),
                RelationsInt(
                    type="开发",
                    description="深度求索开发了DeepSeek MoEs Parse结构以优化计算成本。",
                    head=0,
                    tail=12,
                ),
                RelationsInt(
                    type="接入",
                    description="微软接入了DeepSeek的模型至其云服务中。",
                    head=13,
                    tail=1,
                ),
                RelationsInt(
                    type="接入",
                    description="亚马逊接入了DeepSeek的模型至其云服务中。",
                    head=14,
                    tail=1,
                ),
            ],
        ),
        FirstExtractedGraphData(
            entities=[
                EntityIdInt(text="OpenAI", type="公司", id=0),
                EntityIdInt(text="o1模型", type="产品", id=1),
                EntityIdInt(text="DeepSeek-R1模型", type="产品", id=2),
                EntityIdInt(text="DeepSeek", type="公司", id=3),
                EntityIdInt(text="周鸿祎", type="人物", id=4),
                EntityIdInt(text="纳米AI搜索", type="公司", id=5),
                EntityIdInt(text="华为", type="公司", id=6),
                EntityIdInt(text="阿里", type="公司", id=7),
                EntityIdInt(text="百度", type="公司", id=8),
                EntityIdInt(text="腾讯", type="公司", id=9),
                EntityIdInt(text="京东", type="公司", id=10),
                EntityIdInt(text="小鹏汽车", type="公司", id=11),
                EntityIdInt(text="何小鹏", type="人物", id=12),
            ],
            relations=[
                RelationsInt(
                    type="开发",
                    description="OpenAI 开发了 o1 模型，但该模型不开源、不公布技术细节且收费高。",
                    head=0,
                    tail=1,
                ),
                RelationsInt(
                    type="发布",
                    description="DeepSeek 发布了 DeepSeek-R1 模型，并免费提供给全球用户使用。",
                    head=3,
                    tail=2,
                ),
                RelationsInt(
                    type="合作",
                    description="纳米 AI 搜索与 DeepSeek 建立联系并进行了接入和本地化部署。",
                    head=5,
                    tail=3,
                ),
                RelationsInt(
                    type="提及",
                    description="周鸿祎在纳米 AI 搜索的活动中提到与 DeepSeek 的合作情况。",
                    head=4,
                    tail=5,
                ),
                RelationsInt(
                    type="合作",
                    description="华为宣布接入 DeepSeek 大模型。",
                    head=6,
                    tail=3,
                ),
                RelationsInt(
                    type="合作",
                    description="阿里宣布接入 DeepSeek 大模型。",
                    head=7,
                    tail=3,
                ),
                RelationsInt(
                    type="合作",
                    description="百度宣布接入 DeepSeek 大模型。",
                    head=8,
                    tail=3,
                ),
                RelationsInt(
                    type="合作",
                    description="腾讯宣布接入 DeepSeek 大模型。",
                    head=9,
                    tail=3,
                ),
                RelationsInt(
                    type="合作",
                    description="京东宣布接入 DeepSeek 大模型。",
                    head=10,
                    tail=3,
                ),
                RelationsInt(
                    type="表态",
                    description="何小鹏表示小鹏汽车接入 DeepSeek 大模型是可以期待的。",
                    head=12,
                    tail=11,
                ),
            ],
        ),
    ]
)

import asyncio

from loguru import logger


async def main():
    sub_graph_data_service = SubGraphDataService()
    sub_graph_data_dao = SubGraphDataDAO()
    sub_graph_data_list = [sub_graph_data.model_dump() for sub_graph_data in data.root]
    logger.info(sub_graph_data_list)
    logger.info(len(sub_graph_data_list))
    process_data = await sub_graph_data_dao.batch_create_sub_graph_data(
        id_list=["2222", "33333"],
        text_chunk_id_list=[
            "88ec171b-7d98-45f8-869b-35d7ffa19d31",
            "b34097cb-a760-46d8-963c-aba4057ac1b5",
        ],
        sub_graph_data_list=sub_graph_data_list,
        merged_graph_data_id="e9e7e730-acd6-4ba6-add6-431f795df382",
    )
    return process_data


print(asyncio.run(main()))
