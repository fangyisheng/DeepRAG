# from pydantic import BaseModel


# class Community(BaseModel):
#     community_id: str
#     title: str
#     origin_description: str
#     summary: str


# class DataModel(BaseModel):
#     communities: dict[str, Community]


# # 示例数据
# data = {
#     "610e61ad-5ed5-4514-8a8b-6158d8356cbf": {
#         "title": "深度求索（DeepSeek）的崛起及其对全球AI领域与美股市场的影响",
#         "origin_description": "深度求索（DeepSeek）和全球 AI 领域的关系是深度求索（DeepSeek）在领域中崭露头角全球 AI 领域,深度求索（DeepSeek）在全球 AI 领域成为众人瞩目的焦点。深度求索（DeepSeek）和2023 年的关系是深度求索（DeepSeek）成立于2023 年,深度求索（DeepSeek）成立于2023年。深度求索（DeepSeek）和美股市场的关系是深度求索（DeepSeek）影响力体现在美股市场,深度求索（DeepSeek）的影响力在美股市场有明显体现。深度求索（DeepSeek）和美股 AI、芯片股的关系是深度求索（DeepSeek）被认为是重要因素美股 AI、芯片股,深度求索（DeepSeek）被认为是美股AI、芯片股波动的重要因素之一。",
#         "summary": "深度求索（DeepSeek）是一家成立于2023年的新兴企业，迅速在全球AI领域崭露头角，并成为行业内的焦点。其影响力不仅局限于技术领域，还延伸至美股市场，尤其对美股AI和芯片股的波动产生了重要影响，被视为相关板块变化的关键因素之一。这表明深度求索（DeepSeek）的发展动态已成为资本市场关注的核心议题之一。",
#     },
#     "23bd6c9d-b01e-4822-9d51-74733e60d6b1": {
#         "title": "1月27日美股AI与芯片股重挫事件分析",
#         "origin_description": "1 月 27 日导致重挫美股 AI、芯片股，1月27日，美股AI、芯片股重挫。美股 AI、芯片股影响公司股价英伟达，英伟达收盘大跌超过17%，单日市值蒸发5890亿美元。英伟达创下美国股市历史上最高纪录。深度求索（DeepSeek）被认为是美股AI、芯片股波动的重要因素之一。",
#         "summary": "1月27日，美股AI与芯片股遭遇重挫，其中英伟达受到显著影响，收盘大跌超过17%，单日市值蒸发高达5890亿美元，创下美国股市历史上的最大跌幅记录之一。同时，深度求索（DeepSeek）作为行业内的新兴力量，被认为是此次美股AI及芯片股市场波动的重要因素之一。",
#     },
# }

# # 将数据转换为Pydantic模型
# model_data = DataModel(communities=data)

# print(model_data)


# 假设我们有一个包含字典的列表
list_of_dicts = [{"a": [1, 2]}, {"b": [3, 4]}]

# 要添加的键和值
key_to_append = "c"
value_to_append = 5

for d in list_of_dicts:
    
