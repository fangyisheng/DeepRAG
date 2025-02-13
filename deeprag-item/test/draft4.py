from pyvi import ViGraph

# 定义实体和关系数据
entities = [
    {"id": 0, "text": "张三", "type": "人物"},
    {"id": 1, "text": "上海", "type": "地点"},
    {"id": 2, "text": "建筑工人", "type": "职业"},
    {"id": 3, "text": "李四", "type": "人物"}
]

relations = [
    {"head": 0, "tail": 1, "type": "工作地点"},
    {"head": 0, "tail": 2, "type": "从事职业"},
    {"head": 3, "tail": 0, "type": "别名"}
]

# 创建图对象
graph = ViGraph()

# 添加实体节点
for entity in entities:
    graph.add_node(entity["id"], label=f"{entity['text']} ({entity['type']})")

# 添加关系边
for relation in relations:
    graph.add_edge(relation["head"], relation["tail"], label=relation["type"])

# 可视化图
graph.show()