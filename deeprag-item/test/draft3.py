# text = "2.0.15终端综合     配线箱 integrated  terminal box"

# # 使用 split() 和 join() 清理多余空格
# cleaned_text = " ".join(text.split())
# print(text.split())
# print(cleaned_text)
# import re
# with open("../deeprag/knowledge_file/test.txt","r") as file:
#     content = file.read()
#     print(content)


# content_no_spaces = content.replace(' ', '')
# print(content_no_spaces)

# import re
# text = "2.0.5 贮藏室 storage room \n住宅套内用于贮藏并可以进入的空间\n\n   你们好"
# print(text)
# cleaned_text = text.replace("\n", "")
# print(cleaned_text)
# final_text = cleaned_text = re.sub(r'(?<=[\u4e00-\u9fff\d])\s+|\s+(?=[\u4e00-\u9fff\d])', '', cleaned_text)
# print(final_text)

from pyvis.network import Network
import networkx as nx

# 创建一个空图
G = nx.Graph()

# 添加实体（使用唯一标识符）
G.add_node(1, name="Alice", type="Person")
G.add_node(1, name="Peter", type="Teacher")
G.add_node(2, name="Alice", type="City")  # 同名实体，但类型不同

# 添加边
G.add_edge(1, 3, relation="lives_in")
G.add_edge(2, 3, relation="lives_on")

# 使用 PyVis 可视化
net = Network(notebook=True, cdn_resources="in_line", height="500px", width="100%")

# 将 NetworkX 图转换为 PyVis 图
net.from_nx(G)

# 自定义节点和边的显示
for node in net.nodes:
    node_id = node["id"]
    node_data = G.nodes[node_id]
    node["label"] = f"{node_data['name']} ({node_data['type']})"  # 设置节点标签
    if node_data["type"] == "Person":
        node["color"] = "lightblue"  # 人物节点颜色
    elif node_data["type"] == "City":
        node["color"] = "orange"  # 城市节点颜色

for edge in net.edges:
    u, v = edge["from"], edge["to"]
    edge_data = G.edges[u, v]
    edge["title"] = edge_data["relation"]  # 设置边的提示信息
    edge["color"] = "gray"  # 设置边的颜色

# 显示图形
net.show("knowledge_graph.html")