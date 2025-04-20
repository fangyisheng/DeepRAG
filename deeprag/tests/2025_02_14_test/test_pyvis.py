# from pyvis.network import Network

# # 定义节点和边数据
# nodes = [
#     {'color': '#b5a690', 'text': 'Microsoft', 'type': 'company', 'size': 10,
#      'id': '1a320717-8765-451e-9c1c-6648519d5632', 'label': 'Microsoft (company)',
#      'shape': 'dot', 'font': {'color': 'white'}},
#     {'color': '#b5a690', 'text': 'Azure AI', 'type': 'product', 'size': 10,
#      'id': '0d98dd23-042e-4a28-8cbc-a8050b9d9366', 'label': 'Azure AI (product)',
#      'shape': 'dot', 'font': {'color': 'white'}},
#     {'color': '#b5a690', 'text': 'Satya Nadella', 'type': ['person', 'manager'], 'size': 10,
#      'id': 'ea3432d9-972a-43da-9fab-89a2bb6b950f', 'label': "Satya Nadella (['person', 'manager'])",
#      'shape': 'dot', 'font': {'color': 'white'}}
# ]

# edges = [
#     {'type': ['developed', 'product'], 'width': 1,
#      'from': '1a320717-8765-451e-9c1c-6648519d5632',
#      'to': '0d98dd23-042e-4a28-8cbc-a8050b9d9366',
#      'title': ['developed', 'product'], 'color': '#b5a690'},
#     {'type': 'CEO of', 'width': 1,
#      'from': 'ea3432d9-972a-43da-9fab-89a2bb6b950f',
#      'to': '1a320717-8765-451e-9c1c-6648519d5632',
#      'title': 'CEO of', 'color': '#b5a690'}
# ]

# # 创建一个 pyvis 网络图
# net = Network(notebook=True, directed=True)

# # 添加节点
# for node in nodes:
#     net.add_node(
#         node['id'],
#         label=node['label'],
#         color=node['color'],
#         size=node['size'],
#         shape=node['shape'],
#         font=node['font']
#     )

# # 添加边
# for edge in edges:
#     net.add_edge(
#         edge['from'],
#         edge['to'],
#         title=edge['title'],
#         color=edge['color'],
#         width=edge['width']
#     )

# # 显示并保存图
# net.show("interactive_graph.html")

from pyvis.network import Network

# 创建一个网络图对象
net = Network(notebook=True, cdn_resources="in_line", directed=False)

# 添加节点
net.add_node(1, label="Node 1")
net.add_node(2, label="Node 2")
net.add_node(3, label="Node 3")

# 添加边
net.add_edge(1, 2)
net.add_edge(2, 3)
net.add_edge(3, 1)

# 设置一些可视化选项
net.toggle_physics(True)
# net.show_buttons(filter_=['physics'])  # 显示物理模拟相关的按钮
net.show_buttons(filter_=["physics"])
# 保存为HTML文件
