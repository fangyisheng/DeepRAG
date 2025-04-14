import asyncio
from deeprag.workflow.data_model import (
    GraphDescriptionResponse,
    GraphDescriptionWithCommunityClusterResponse,
    CompleteGraphData,
    EntityIdStr,
    RelationsStr,
    CompleteGraphDataWithCommunityId,
)


class GraphDescription:
    # 今天3月7日要改完这个bug
    def __init__(self):
        pass

    async def describe_graph(
        self, graph: CompleteGraphData
    ) -> GraphDescriptionResponse:
        """_summary_

        Args:
            graph (dict): 图的结构是个dict

        Returns:
            list[str]: 由图的结构扩展出来的关系描述文本列表
        """
        graph = graph.model_dump()
        graph_description_list = []
        for relation in graph["relations"]:
            relation_head_text = next(
                (
                    entity["text"]
                    for entity in graph["entities"]
                    if entity["id"] == relation["head"]
                ),
                None,
            )
            relation_tail_text = next(
                (
                    entity["text"]
                    for entity in graph["entities"]
                    if entity["id"] == relation["tail"]
                ),
                None,
            )

            if isinstance(relation["type"], str):
                graph_description = f"{relation_head_text}和{relation_tail_text}的关系是{relation_head_text}{relation['type']}{relation_tail_text},{relation['description']}"
                graph_description_list.append(graph_description)
            else:
                for type in relation["type"]:
                    graph_description = f"{relation_head_text}和{relation_tail_text}的关系是{relation_head_text}{type}{relation_tail_text},{relation['description']}"
                    graph_description_list.append(graph_description)

        return GraphDescriptionResponse(root=graph_description_list)

    # 这个函数负责搞定给关系描述的文本块提供属于哪个社区的信息
    """ 怎么去区分这个描述文本块属于哪个社区的逻辑是：如果一个关系中的两个实体是来自同一个社区id的，那么这个描述文本块也来自同一个社区id，如果遇到
    一个关系中，两个实体来自不同的社区id，那么先判断哪个社区id已经被保存在了community_id_list中，没有被保存的那个社区id就是这个关系的社区id"""

    async def describe_graph_with_community_cluster(
        self, graph: CompleteGraphDataWithCommunityId
    ) -> GraphDescriptionWithCommunityClusterResponse:
        """_summary_

        Args:
            graph (dict): 完整的图的结构(带有community_id)

        Returns:
            dict[str, list]: 带有community_id为键，关系描述文本列表为值的dict
        """
        graph = graph.model_dump()
        relation_community_id_list = {}
        for relation in graph["relations"]:
            relation_head_community_id = next(
                (
                    entity["community_id"]
                    for entity in graph["entities"]
                    if relation["head"] == entity["id"]
                ),
                None,
            )
            relation_tail_community_id = next(
                (
                    entity["community_id"]
                    for entity in graph["entities"]
                    if relation["tail"] == entity["id"]
                ),
                None,
            )
            relation_head_text = next(
                (
                    entity["text"]
                    for entity in graph["entities"]
                    if entity["id"] == relation["head"]
                ),
                None,
            )
            relation_tail_text = next(
                (
                    entity["text"]
                    for entity in graph["entities"]
                    if entity["id"] == relation["tail"]
                ),
                None,
            )
            if isinstance(relation["type"], str):
                graph_description = f"{relation_head_text}和{relation_tail_text}的关系是{relation_head_text}{relation['type']}{relation_tail_text},{relation['description']}"
                if relation_head_community_id == relation_tail_community_id:
                    relation_community_id_list.setdefault(
                        relation_head_community_id, []
                    ).append(graph_description)
                else:
                    relation_community_id_list.setdefault(
                        relation_head_community_id, []
                    ).append(graph_description)
                    relation_community_id_list.setdefault(
                        relation_tail_community_id, []
                    ).append(graph_description)

            else:
                graph_description_list = []
                for type in relation["type"]:
                    graph_description = f"{relation_head_text}和{relation_tail_text}的关系是{relation_head_text}{type}{relation_tail_text},{relation['description']}"
                    graph_description_list.append(graph_description)
                if relation_head_community_id == relation_tail_community_id:
                    relation_community_id_list.setdefault(
                        relation_head_community_id, []
                    ).extend(graph_description_list)
                else:
                    relation_community_id_list.setdefault(
                        relation_head_community_id, []
                    ).extend(graph_description_list)
                    relation_community_id_list.setdefault(
                        relation_tail_community_id, []
                    ).extend(graph_description_list)
        return GraphDescriptionWithCommunityClusterResponse(
            root=relation_community_id_list
        )

    # async def describe_graph_with_community_cluster(self, graph: dict):
    #     relation_community_id_list = []
    #     for relation in graph["relations"]:
    #         relation_head_community_id = next(
    #             (
    #                 entity["community_id"]
    #                 for entity in graph["entities"]
    #                 if relation["head"] == entity["id"]
    #             ),
    #             None,
    #         )
    #         relation_tail_community_id = next(
    #             (
    #                 entity["community_id"]
    #                 for entity in graph["entities"]
    #                 if relation["tail"] == entity["id"]
    #             ),
    #             None,
    #         )
    #         relation_head_text = next(
    #             (
    #                 entity["text"]
    #                 for entity in graph["entities"]
    #                 if entity["id"] == relation["head"]
    #             ),
    #             None,
    #         )
    #         relation_tail_text = next(
    #             (
    #                 entity["text"]
    #                 for entity in graph["entities"]
    #                 if entity["id"] == relation["tail"]
    #             ),
    #             None,
    #         )
    #         if isinstance(relation["type"], str):
    #             graph_description = f"{relation_head_text}和{relation_tail_text}的关系是{relation_head_text}{relation['type']}{relation_tail_text},{relation['description']}"
    #             if relation_head_community_id == relation_tail_community_id:

    #                 if relation_community_id_list:
    #                     for relation_community in relation_community_id_list:
    #                         if relation_head_community_id == relation_community["community_id"]

    #                 else:
    #                     new_dict = {"community_id": relation_head_community_id}
    #                     new_dict.setdefault(
    #                     "graph_description", []
    #                 ).append(graph_description)
    #                     relation_community_id_list.append(
    #                     new_dict
    #                 )

    #             else:
    #                 relation_community_id_list.setdefault(
    #                     relation_head_community_id, []
    #                 ).append(graph_description)
    #                 relation_community_id_list.setdefault(
    #                     relation_tail_community_id, []
    #                 ).append(graph_description)

    #         else:
    #             graph_description_list = []
    #             for type in relation["type"]:
    #                 graph_description = f"{relation_head_text}和{relation_tail_text}的关系是{relation_head_text}{type}{relation_tail_text},{relation['description']}"
    #                 graph_description_list.append(graph_description)
    #             if relation_head_community_id == relation_tail_community_id:
    #                 relation_community_id_list.setdefault(
    #                     relation_head_community_id, []
    #                 ).extend(graph_description_list)
    #             else:
    #                 relation_community_id_list.setdefault(
    #                     relation_head_community_id, []
    #                 ).extend(graph_description_list)
    #                 relation_community_id_list.setdefault(
    #                     relation_tail_community_id, []
    #                 ).extend(graph_description_list)
    #     return relation_community_id_list


# 测试数据
test_data = CompleteGraphDataWithCommunityId(
    entities=[
        EntityIdStr(
            text="深度求索", type="组织", id="ccdafe4c-525c-4dd0-9a32-31fde645c4f7"
        ),
        EntityIdStr(
            text="DeepSeek",
            type=["产品", "组织"],
            id="e75f2ebb-c163-4274-8dc7-0a4b5aeca293",
        ),
        EntityIdStr(
            text="AI领域", type="领域", id="36fb7181-ca89-4054-b9c4-f3b5821c1a24"
        ),
        EntityIdStr(
            text="美股市场", type="地点", id="c0d60634-ca08-4d08-a853-001098ba2f41"
        ),
        EntityIdStr(
            text="英伟达", type="组织", id="f431fb94-7729-4f3f-97bf-61f7dbb3d6a3"
        ),
        EntityIdStr(
            text="幻方量化", type="组织", id="6adc7c90-44c0-4815-86e0-bdc189d72ef8"
        ),
        EntityIdStr(
            text="OpenAI", type="组织", id="de2e9d09-0088-4aaa-b7ec-3e3481ff2e4b"
        ),
        EntityIdStr(
            text="GPT-4o", type="产品", id="72cf64f6-302e-4bc9-9145-9f88d10b3dcb"
        ),
        EntityIdStr(
            text="华为云", type="产品", id="72b94856-8fa1-4003-83a8-a99c8e4521ef"
        ),
        EntityIdStr(
            text="腾讯云", type="产品", id="0da7a1d1-1e06-4a40-85ed-c980daccc793"
        ),
        EntityIdStr(
            text="百度云", type="产品", id="b104041f-5892-47df-a817-00ac9413f696"
        ),
        EntityIdStr(
            text="MLA架构", type="技术", id="b4e0209a-90a2-46ea-b4c8-6b9f94b82668"
        ),
        EntityIdStr(
            text="MHA架构", type="技术", id="55f4feeb-0f22-41e9-b980-774dd2224b1a"
        ),
        EntityIdStr(
            text="DeepSeek MoEs Parse结构",
            type="技术",
            id="5d7dc46c-0a13-4c27-b1ad-74cc9d37a8b7",
        ),
        EntityIdStr(
            text="DeepSeek-R1模型",
            type="产品",
            id="3b6589ff-e7a1-49de-9930-ae0f9401a426",
        ),
        EntityIdStr(
            text="清华大学", type="地点", id="bfcdbe19-9b08-4c39-af81-1b0673606e4a"
        ),
        EntityIdStr(
            text="A大学", type="地点", id="50f97e53-a703-4180-ba15-6bb17d713f15"
        ),
        EntityIdStr(
            text="硅谷", type="地点", id="61f47b6d-fbe1-4fca-babe-41ad826ef181"
        ),
        EntityIdStr(text="o1", type="模型", id="2aea64b1-17eb-4e58-926b-78df5ae4e3c2"),
        EntityIdStr(
            text="DeepSeek-R1", type="模型", id="147551da-12fb-48c5-8606-d5c778934a32"
        ),
        EntityIdStr(
            text="周鸿祎", type="人物", id="3be97db1-0a78-428e-90f5-8f9486e3058c"
        ),
        EntityIdStr(
            text="纳米 AI 搜索", type="产品", id="ae38f7cb-6d00-455f-a0cb-1b7fe7742cb9"
        ),
        EntityIdStr(
            text="小鹏汽车", type="组织", id="92dd4cc3-1165-41ff-9202-e05498b78817"
        ),
        EntityIdStr(
            text="何小鹏", type="人物", id="f99ab180-a5e9-43ed-83ec-b953b2bfb7b1"
        ),
        EntityIdStr(
            text="华为", type="组织", id="f8db8fbf-8a69-442e-a5d5-7c3628d9f271"
        ),
        EntityIdStr(
            text="阿里", type="组织", id="564419fc-5b01-4747-a0a0-4d2b5fd7cad9"
        ),
        EntityIdStr(
            text="百度", type="组织", id="71cd4cbb-7a43-4709-b0d1-4c6f3547e577"
        ),
        EntityIdStr(
            text="腾讯", type="组织", id="603ae5e0-6da4-452c-bb88-cd837509511b"
        ),
        EntityIdStr(
            text="京东", type="组织", id="23ae2024-979a-4e5e-86c7-cff0fdd2711d"
        ),
    ],
    relations=[
        RelationsStr(
            type="开发",
            description="深度求索开发了DeepSeek。",
            id="68057761-9cdc-4f70-a9f2-c3f0b50f9b5a",
            head="ccdafe4c-525c-4dd0-9a32-31fde645c4f7",
            tail="e75f2ebb-c163-4274-8dc7-0a4b5aeca293",
        ),
        RelationsStr(
            type="属于",
            description="DeepSeek属于AI领域。",
            id="4d195c86-cd73-4e39-8e8f-26b12f7be3b9",
            head="e75f2ebb-c163-4274-8dc7-0a4b5aeca293",
            tail="36fb7181-ca89-4054-b9c4-f3b5821c1a24",
        ),
        RelationsStr(
            type="影响",
            description="DeepSeek在美股市场产生影响。",
            id="c3343b33-5f13-46aa-9202-4bc0e53e7fd3",
            head="e75f2ebb-c163-4274-8dc7-0a4b5aeca293",
            tail="c0d60634-ca08-4d08-a853-001098ba2f41",
        ),
        RelationsStr(
            type="上市",
            description="英伟达在美股市场上市。",
            id="38324f65-948a-45a9-80de-2e40e48f3d2b",
            head="f431fb94-7729-4f3f-97bf-61f7dbb3d6a3",
            tail="c0d60634-ca08-4d08-a853-001098ba2f41",
        ),
        RelationsStr(
            type="孵化",
            description="幻方量化孵化了深度求索。",
            id="d8544da8-d7e6-4d46-8e06-46aae3f844a6",
            head="6adc7c90-44c0-4815-86e0-bdc189d72ef8",
            tail="ccdafe4c-525c-4dd0-9a32-31fde645c4f7",
        ),
        RelationsStr(
            type="开发",
            description="OpenAI开发了GPT-4o。",
            id="aaa14331-ed90-4658-bfe7-84f1b00863fc",
            head="de2e9d09-0088-4aaa-b7ec-3e3481ff2e4b",
            tail="72cf64f6-302e-4bc9-9145-9f88d10b3dcb",
        ),
        RelationsStr(
            type="合作",
            description="华为云与DeepSeek合作。",
            id="070af30d-060e-48e4-929d-cb55793d42dc",
            head="72b94856-8fa1-4003-83a8-a99c8e4521ef",
            tail="e75f2ebb-c163-4274-8dc7-0a4b5aeca293",
        ),
        RelationsStr(
            type="合作",
            description="腾讯云与DeepSeek合作。",
            id="da474c59-3f79-4cfa-b630-e43ed6624635",
            head="0da7a1d1-1e06-4a40-85ed-c980daccc793",
            tail="e75f2ebb-c163-4274-8dc7-0a4b5aeca293",
        ),
        RelationsStr(
            type="合作",
            description="百度云与DeepSeek合作。",
            id="8e432e8f-ac3c-4db6-96f1-6d431cbefdc1",
            head="b104041f-5892-47df-a817-00ac9413f696",
            tail="e75f2ebb-c163-4274-8dc7-0a4b5aeca293",
        ),
        RelationsStr(
            type="提出",
            description="深度求索提出了MLA架构。",
            id="ec4e8529-b87f-490d-9254-f47dae1b7ffb",
            head="b4e0209a-90a2-46ea-b4c8-6b9f94b82668",
            tail="ccdafe4c-525c-4dd0-9a32-31fde645c4f7",
        ),
        RelationsStr(
            type="采用",
            description="深度求索采用了DeepSeek MoEs Parse结构。",
            id="48ba043d-417e-44d7-a4d3-712b01c7d1e8",
            head="5d7dc46c-0a13-4c27-b1ad-74cc9d37a8b7",
            tail="ccdafe4c-525c-4dd0-9a32-31fde645c4f7",
        ),
        RelationsStr(
            type="开发",
            description="深度求索开发了DeepSeek-R1模型。",
            id="5d7ab131-4c44-4822-83ea-16af492bdfba",
            head="3b6589ff-e7a1-49de-9930-ae0f9401a426",
            tail="ccdafe4c-525c-4dd0-9a32-31fde645c4f7",
        ),
        RelationsStr(
            type="对比",
            description="DeepSeek-R1模型对清华大学和A大学进行对比。",
            id="5a212885-ce73-485e-aed5-fd312e6fa0a0",
            head="bfcdbe19-9b08-4c39-af81-1b0673606e4a",
            tail="50f97e53-a703-4180-ba15-6bb17d713f15",
        ),
        RelationsStr(
            type="认可",
            description="硅谷认可了深度求索的技术实力。",
            id="55adb057-58f4-4054-94e5-1b15b63778d0",
            head="61f47b6d-fbe1-4fca-babe-41ad826ef181",
            tail="ccdafe4c-525c-4dd0-9a32-31fde645c4f7",
        ),
        RelationsStr(
            type="隶属于",
            description="o1模型由OpenAI开发",
            id="6603841a-9a99-44aa-b63a-8ca24d148039",
            head="2aea64b1-17eb-4e58-926b-78df5ae4e3c2",
            tail="de2e9d09-0088-4aaa-b7ec-3e3481ff2e4b",
        ),
        RelationsStr(
            type="隶属于",
            description="DeepSeek-R1模型由DeepSeek发布",
            id="ead03ca9-669d-411f-88b4-b4eec66ec72d",
            head="147551da-12fb-48c5-8606-d5c778934a32",
            tail="e75f2ebb-c163-4274-8dc7-0a4b5aeca293",
        ),
        RelationsStr(
            type="参与",
            description="周鸿祎参与纳米AI搜索活动并提到与DeepSeek的合作",
            id="080daa7b-1bbd-4b33-9789-d27e9b3bee01",
            head="3be97db1-0a78-428e-90f5-8f9486e3058c",
            tail="ae38f7cb-6d00-455f-a0cb-1b7fe7742cb9",
        ),
        RelationsStr(
            type="合作",
            description="纳米AI搜索与DeepSeek建立联系并进行本地化部署",
            id="ecb4f789-4acd-4e9a-b34c-e8fab33f4b1a",
            head="ae38f7cb-6d00-455f-a0cb-1b7fe7742cb9",
            tail="e75f2ebb-c163-4274-8dc7-0a4b5aeca293",
        ),
        RelationsStr(
            type="可能合作",
            description="小鹏汽车可能接入DeepSeek大模型",
            id="0b8064f2-4946-440a-8c43-1a1d996b73a5",
            head="92dd4cc3-1165-41ff-9202-e05498b78817",
            tail="e75f2ebb-c163-4274-8dc7-0a4b5aeca293",
        ),
        RelationsStr(
            type="担任",
            description="何小鹏担任小鹏汽车董事长",
            id="d3dd0124-7ae3-4ca4-b2ae-d208d21ea9e3",
            head="f99ab180-a5e9-43ed-83ec-b953b2bfb7b1",
            tail="92dd4cc3-1165-41ff-9202-e05498b78817",
        ),
        RelationsStr(
            type="合作",
            description="华为宣布接入DeepSeek大模型",
            id="1eb77f3f-3bbc-4bda-9fcd-06b1bc674b5b",
            head="f8db8fbf-8a69-442e-a5d5-7c3628d9f271",
            tail="e75f2ebb-c163-4274-8dc7-0a4b5aeca293",
        ),
        RelationsStr(
            type="合作",
            description="阿里宣布接入DeepSeek大模型",
            id="bbb7b666-99f9-49f5-b09c-f6fdb215cff4",
            head="564419fc-5b01-4747-a0a0-4d2b5fd7cad9",
            tail="e75f2ebb-c163-4274-8dc7-0a4b5aeca293",
        ),
        RelationsStr(
            type="合作",
            description="百度宣布接入DeepSeek大模型",
            id="4c01a145-c996-46a5-bba1-5132d380b61a",
            head="71cd4cbb-7a43-4709-b0d1-4c6f3547e577",
            tail="e75f2ebb-c163-4274-8dc7-0a4b5aeca293",
        ),
        RelationsStr(
            type="合作",
            description="腾讯宣布接入DeepSeek大模型",
            id="04450fa5-6c63-4ca9-b6ea-39d3b2b05c57",
            head="603ae5e0-6da4-452c-bb88-cd837509511b",
            tail="e75f2ebb-c163-4274-8dc7-0a4b5aeca293",
        ),
        RelationsStr(
            type="合作",
            description="京东宣布接入DeepSeek大模型",
            id="73cf9fec-a0a7-4a47-a8a6-f5c581260e9f",
            head="23ae2024-979a-4e5e-86c7-cff0fdd2711d",
            tail="e75f2ebb-c163-4274-8dc7-0a4b5aeca293",
        ),
    ],
)


graph_description = GraphDescription()
# print(asyncio.run(graph_description.describe_graph_with_community_cluster(test_data)))
print(asyncio.run(graph_description.describe_graph(test_data)))
print(asyncio.run(graph_description.describe_graph_with_community_cluster(test_data)))
