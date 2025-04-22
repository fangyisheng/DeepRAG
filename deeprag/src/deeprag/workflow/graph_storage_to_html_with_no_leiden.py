import networkx as nx
from pyvis.network import Network
import random
import asyncio
import uuid
import igraph as ig
from deeprag.workflow.data_model import (
    GraphDataWithVisualization,
    CompleteGraphData,
    EntityIdStr,
    RelationsStr,
)
from deeprag.workflow.upload_file_to_minio import upload_file_to_minio_func


async def store_graph_data_to_html_with_no_leiden(
    entity_relationship: CompleteGraphData,
) -> GraphDataWithVisualization:
    # 创建有向关系图 如果是nx.Graph()则是创建了无向图，(u,v)和(v,u)等价
    G = nx.DiGraph()
    # 存储实体和实体之间的关系
    entity_relationship = entity_relationship.model_dump()
    for entity in entity_relationship["entities"]:
        G.add_node(entity["id"], text=entity["text"], type=entity["type"])

    for relation in entity_relationship["relations"]:
        G.add_edge(relation["head"], relation["tail"], type=relation["type"])

    # G的数据格式没问题了

    # 使用 PyVis 可视化
    net = Network(
        notebook=True,
        cdn_resources="in_line",
        height="750px",
        width="100%",
        bgcolor="#222222",
        font_color="white",
        directed=True,
    )
    net.set_options("""
    {
    "physics": {
        "enabled": true,
        "barnesHut": {
        "gravitationalConstant": -2000,
        "springLength": 400,
        "springConstant": 0.04
        },
        "minVelocity": 0.75,
        "stabilization": {
        "enabled": true,
        "iterations": 1000,
        "updateInterval": 100,
        "onlyDynamicEdges": false,
        "fit": true
        }
    }
    }
    """)

    # 将 NetworkX 图转换为 PyVis 图
    net.from_nx(G)

    color = f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
    # # 自定义节点和边的显示
    for node in net.nodes:
        # 在pyvis中label字段用于节点的显示标签，如果没有这个label，就会取node的id字段，通常id字段都是uuid什么的，容易不太好看，所以设置一下label标签
        node["label"] = f"{node['text']} ({node['type']})"  # 设置节点标签
        node["color"] = color
    for edge in net.edges:
        if len(edge["type"]) > 1:
            edge["label"] = str(edge["type"])  # 设置边的提示信息
        else:
            edge["label"] = edge["type"]
        edge["color"] = color

    # prefix = str(uuid.uuid4())
    # # 这块net.show先保留了，方便以后做测试
    # net.show(f"{prefix}_graph_with_no_leiden.html")
    html_content = net.generate_html()

    # 然后需要把这点字符串上传到minio中，方便下载查看

    return GraphDataWithVisualization(root=html_content)


# # 编写测试代码
# import asyncio

# test_data = CompleteGraphData(
#     entities=[
#         EntityIdStr(
#             text="深度求索", type="组织", id="41ad744b-be5d-48b2-b271-40a5fb656e52"
#         ),
#         EntityIdStr(
#             text="DeepSeek",
#             type=["产品", "组织"],
#             id="b01f6811-69fe-4956-9921-a406230473d4",
#         ),
#         EntityIdStr(
#             text="AI领域", type="领域", id="ae40602e-247b-4b2a-a70b-4ee99e45a81f"
#         ),
#         EntityIdStr(
#             text="美股市场", type="地点", id="805bf8d9-91ae-4cab-b699-8586ef0935de"
#         ),
#         EntityIdStr(
#             text="英伟达", type="组织", id="7988d0dc-702f-4113-88ec-2862bf17ae06"
#         ),
#         EntityIdStr(
#             text="幻方量化", type="组织", id="58fde335-b7cf-417e-af0a-38a4d26ff5a2"
#         ),
#         EntityIdStr(
#             text="OpenAI", type="组织", id="aaa765fa-e567-47af-af36-aa37ded6ab47"
#         ),
#         EntityIdStr(
#             text="GPT-4o", type="产品", id="614eee62-a2d2-456c-9abe-aeb8e72558f6"
#         ),
#         EntityIdStr(
#             text="华为云", type="产品", id="9858285d-11f9-488e-b0d5-1dfa24b6c036"
#         ),
#         EntityIdStr(
#             text="腾讯云", type="产品", id="cbfc10b3-e947-4612-aba7-c876d9401dd9"
#         ),
#         EntityIdStr(
#             text="百度云", type="产品", id="5a520449-0863-4f82-b452-62a9418b07b0"
#         ),
#         EntityIdStr(
#             text="MLA架构", type="技术", id="49483ca0-73a7-49c6-984b-f118ecb33447"
#         ),
#         EntityIdStr(
#             text="MHA架构", type="技术", id="05359cd6-2815-4f28-9f96-7280f7d406d7"
#         ),
#         EntityIdStr(
#             text="DeepSeek MoEs Parse结构",
#             type="技术",
#             id="146eee1c-aca0-4ac2-ae62-677734ee298d",
#         ),
#         EntityIdStr(
#             text="DeepSeek-R1模型",
#             type="产品",
#             id="a00b06ef-577f-4342-914c-9e15fa45c2d0",
#         ),
#         EntityIdStr(
#             text="清华大学", type="地点", id="18c1c8b3-c1eb-4132-a349-ecbc056036d4"
#         ),
#         EntityIdStr(
#             text="A大学", type="地点", id="780e056c-d1b1-49f0-8872-0c13bdacde50"
#         ),
#         EntityIdStr(
#             text="硅谷", type="地点", id="2efdd18e-ad74-4d60-8176-b1567ebce7b2"
#         ),
#         EntityIdStr(text="o1", type="模型", id="e9c65074-3ee7-4413-8720-19e6ed9d38dc"),
#         EntityIdStr(
#             text="DeepSeek-R1", type="模型", id="a48877e9-3bc8-4b04-8224-d891cddc8c30"
#         ),
#         EntityIdStr(
#             text="周鸿祎", type="人物", id="3ed5bf31-a265-40b6-8a89-e3822281e564"
#         ),
#         EntityIdStr(
#             text="纳米 AI 搜索", type="产品", id="587ac2b5-0cf2-4b29-b1dc-2091fde8f69f"
#         ),
#         EntityIdStr(
#             text="小鹏汽车", type="组织", id="7ad53021-7f0d-4fef-9275-a7a3d51b59b2"
#         ),
#         EntityIdStr(
#             text="何小鹏", type="人物", id="7d93a679-a3a1-49e0-9faf-18642c140aa3"
#         ),
#         EntityIdStr(
#             text="华为", type="组织", id="0613d969-960f-424d-b904-915c59c8ad0b"
#         ),
#         EntityIdStr(
#             text="阿里", type="组织", id="2cba8b5f-db14-4f46-a6d7-0189b94a0882"
#         ),
#         EntityIdStr(
#             text="百度", type="组织", id="5c49aed2-dffc-4e60-9386-5d3ab08de0d7"
#         ),
#         EntityIdStr(
#             text="腾讯", type="组织", id="1c89170e-dc17-4745-ad85-3741ba307b1e"
#         ),
#         EntityIdStr(
#             text="京东", type="组织", id="5f81d12c-5b7d-427b-81bd-fe34dd501054"
#         ),
#     ],
#     relations=[
#         RelationsStr(
#             type="开发",
#             description="深度求索开发了DeepSeek。",
#             id="7211c051-0fc8-47e1-9551-435a5e6b2fbe",
#             head="41ad744b-be5d-48b2-b271-40a5fb656e52",
#             tail="b01f6811-69fe-4956-9921-a406230473d4",
#         ),
#         RelationsStr(
#             type="属于",
#             description="DeepSeek属于AI领域。",
#             id="49f2dc53-d3c6-457e-a440-5215a06782fa",
#             head="b01f6811-69fe-4956-9921-a406230473d4",
#             tail="ae40602e-247b-4b2a-a70b-4ee99e45a81f",
#         ),
#         RelationsStr(
#             type="影响",
#             description="DeepSeek在美股市场产生影响。",
#             id="192122e8-101d-4d2d-8be9-5e26615fdd8b",
#             head="b01f6811-69fe-4956-9921-a406230473d4",
#             tail="805bf8d9-91ae-4cab-b699-8586ef0935de",
#         ),
#         RelationsStr(
#             type="上市",
#             description="英伟达在美股市场上市。",
#             id="dc293d99-c9d6-4148-831d-372dc39f6da9",
#             head="7988d0dc-702f-4113-88ec-2862bf17ae06",
#             tail="805bf8d9-91ae-4cab-b699-8586ef0935de",
#         ),
#         RelationsStr(
#             type="孵化",
#             description="幻方量化孵化了深度求索。",
#             id="39060376-7320-4bea-be8d-5191ed1837af",
#             head="58fde335-b7cf-417e-af0a-38a4d26ff5a2",
#             tail="41ad744b-be5d-48b2-b271-40a5fb656e52",
#         ),
#         RelationsStr(
#             type="开发",
#             description="OpenAI开发了GPT-4o。",
#             id="f47d55c6-c269-4660-8f0c-7a8b2532abf2",
#             head="aaa765fa-e567-47af-af36-aa37ded6ab47",
#             tail="614eee62-a2d2-456c-9abe-aeb8e72558f6",
#         ),
#         RelationsStr(
#             type="合作",
#             description="华为云与DeepSeek合作。",
#             id="635aa35f-796e-45a0-90a5-956c047ff37f",
#             head="9858285d-11f9-488e-b0d5-1dfa24b6c036",
#             tail="b01f6811-69fe-4956-9921-a406230473d4",
#         ),
#         RelationsStr(
#             type="合作",
#             description="腾讯云与DeepSeek合作。",
#             id="1b882e24-e790-49ca-9890-4e434a60c52f",
#             head="cbfc10b3-e947-4612-aba7-c876d9401dd9",
#             tail="b01f6811-69fe-4956-9921-a406230473d4",
#         ),
#         RelationsStr(
#             type="合作",
#             description="百度云与DeepSeek合作。",
#             id="eaf969a8-7e55-4655-a0ae-646d0e5fde42",
#             head="5a520449-0863-4f82-b452-62a9418b07b0",
#             tail="b01f6811-69fe-4956-9921-a406230473d4",
#         ),
#         RelationsStr(
#             type="提出",
#             description="深度求索提出了MLA架构。",
#             id="106dac4c-6a73-42e9-95f4-375be1468d40",
#             head="49483ca0-73a7-49c6-984b-f118ecb33447",
#             tail="41ad744b-be5d-48b2-b271-40a5fb656e52",
#         ),
#         RelationsStr(
#             type="采用",
#             description="深度求索采用了DeepSeek MoEs Parse结构。",
#             id="4cfbc244-d1c9-4025-8142-eaaf261f9c7c",
#             head="146eee1c-aca0-4ac2-ae62-677734ee298d",
#             tail="41ad744b-be5d-48b2-b271-40a5fb656e52",
#         ),
#         RelationsStr(
#             type="开发",
#             description="深度求索开发了DeepSeek-R1模型。",
#             id="4467259d-c04f-4cff-8105-5cc0c6e7e3d3",
#             head="a00b06ef-577f-4342-914c-9e15fa45c2d0",
#             tail="41ad744b-be5d-48b2-b271-40a5fb656e52",
#         ),
#         RelationsStr(
#             type="对比",
#             description="DeepSeek-R1模型对清华大学和A大学进行对比。",
#             id="22d0fded-9f1d-4c9b-8ecc-6d8c0c6bffab",
#             head="18c1c8b3-c1eb-4132-a349-ecbc056036d4",
#             tail="780e056c-d1b1-49f0-8872-0c13bdacde50",
#         ),
#         RelationsStr(
#             type="认可",
#             description="硅谷认可了深度求索的技术实力。",
#             id="407b200b-e433-4cfa-83c6-694d177dab81",
#             head="2efdd18e-ad74-4d60-8176-b1567ebce7b2",
#             tail="41ad744b-be5d-48b2-b271-40a5fb656e52",
#         ),
#         RelationsStr(
#             type="隶属于",
#             description="o1模型由OpenAI开发",
#             id="f0b3c997-288c-445a-81e3-71e50c447aa3",
#             head="e9c65074-3ee7-4413-8720-19e6ed9d38dc",
#             tail="aaa765fa-e567-47af-af36-aa37ded6ab47",
#         ),
#         RelationsStr(
#             type="隶属于",
#             description="DeepSeek-R1模型由DeepSeek发布",
#             id="97502af8-f549-4ba5-8f1c-d1c54acd684d",
#             head="a48877e9-3bc8-4b04-8224-d891cddc8c30",
#             tail="b01f6811-69fe-4956-9921-a406230473d4",
#         ),
#         RelationsStr(
#             type="参与",
#             description="周鸿祎参与纳米AI搜索活动并提到与DeepSeek的合作",
#             id="c0bb4e4a-1a93-405d-8e3a-78d6b1de86a1",
#             head="3ed5bf31-a265-40b6-8a89-e3822281e564",
#             tail="587ac2b5-0cf2-4b29-b1dc-2091fde8f69f",
#         ),
#         RelationsStr(
#             type="合作",
#             description="纳米AI搜索与DeepSeek建立联系并进行本地化部署",
#             id="a1ecc0d9-7d9b-4a55-b8ff-b5c362306d9e",
#             head="587ac2b5-0cf2-4b29-b1dc-2091fde8f69f",
#             tail="b01f6811-69fe-4956-9921-a406230473d4",
#         ),
#         RelationsStr(
#             type="可能合作",
#             description="小鹏汽车可能接入DeepSeek大模型",
#             id="6c53f571-ef5d-46f0-8367-9093f72c221c",
#             head="7ad53021-7f0d-4fef-9275-a7a3d51b59b2",
#             tail="b01f6811-69fe-4956-9921-a406230473d4",
#         ),
#         RelationsStr(
#             type="担任",
#             description="何小鹏担任小鹏汽车董事长",
#             id="27628046-5268-449a-9a19-87c4e97e8f51",
#             head="7d93a679-a3a1-49e0-9faf-18642c140aa3",
#             tail="7ad53021-7f0d-4fef-9275-a7a3d51b59b2",
#         ),
#         RelationsStr(
#             type="合作",
#             description="华为宣布接入DeepSeek大模型",
#             id="49657e56-317a-4e15-be6b-363c9d8129d8",
#             head="0613d969-960f-424d-b904-915c59c8ad0b",
#             tail="b01f6811-69fe-4956-9921-a406230473d4",
#         ),
#         RelationsStr(
#             type="合作",
#             description="阿里宣布接入DeepSeek大模型",
#             id="9869d577-8732-4bf9-85c5-a2c0f67dabd1",
#             head="2cba8b5f-db14-4f46-a6d7-0189b94a0882",
#             tail="b01f6811-69fe-4956-9921-a406230473d4",
#         ),
#         RelationsStr(
#             type="合作",
#             description="百度宣布接入DeepSeek大模型",
#             id="b1ba74e6-1777-4216-bb90-f40964a42265",
#             head="5c49aed2-dffc-4e60-9386-5d3ab08de0d7",
#             tail="b01f6811-69fe-4956-9921-a406230473d4",
#         ),
#         RelationsStr(
#             type="合作",
#             description="腾讯宣布接入DeepSeek大模型",
#             id="ef865222-fada-43b4-b139-6aff7a8f9b09",
#             head="1c89170e-dc17-4745-ad85-3741ba307b1e",
#             tail="b01f6811-69fe-4956-9921-a406230473d4",
#         ),
#         RelationsStr(
#             type="合作",
#             description="京东宣布接入DeepSeek大模型",
#             id="1fde2c65-a13e-45c8-938c-06a427c17693",
#             head="5f81d12c-5b7d-427b-81bd-fe34dd501054",
#             tail="b01f6811-69fe-4956-9921-a406230473d4",
#         ),
#     ],
# )

# print(asyncio.run(store_graph_data_to_html_with_no_leiden(test_data)))
