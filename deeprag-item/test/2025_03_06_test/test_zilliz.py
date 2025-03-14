# 这个测试文件只测试文本分块和对应的embedding向量怎么嵌入到zilliz的向量数据库中


from deeprag.workflow.vector_with_text_to_vector_db import data_insert_to_vector_db
from deeprag.rag_core_utils.embedding_api.embedding_api_client import text_to_vector
from deeprag.rag_core_utils.vector_db_api.vector_db_api_client import (
    create_or_use_hybrid_search_milvus_client_collection,
)
from deeprag.rag_core_utils.vector_db_api.vector_db_api_client import (
    create_or_use_hybrid_search_milvus_client_collection,
)
from loguru import logger

# async def main(mock_data):
#     vector_list = await text_to_vector(mock_data)
#     logger.info(vector_list)
#     meta_data =  ["""{"doc_title":"test.txt"}""" for _ in mock_data]
#     res = await data_insert_to_vector_db(mock_data,vector_list,meta_data)
#     return res


# import asyncio
# mock_data = ['深度求索（DeepSeek）和全球 AI 领域的关系是深度求索（DeepSeek）在领域中崭露头角全球 AI 领域,深度求索（DeepSeek）在全球 AI 领域成为众人瞩目的焦点。', '深度求索（DeepSeek）和2023 年的关系是深度求索（DeepSeek）成立于2023 年,深度求索（DeepSeek）成立于2023年。', '深度求索（DeepSeek）和美股市场的关系是深度求索（DeepSeek）影响力体现在美股市场,深度求索（DeepSeek）的影响力在美股市场有明显体现。', '1 月 27 日和美股 AI、芯片股的关系是1 月 27 日导致重挫美股 AI、芯片股,1月27日，美股AI、芯片股重挫。', '美股 AI、芯片股和英伟达的关系是美股 AI、芯片股影响公司股价英伟达,英伟达收盘大跌超过17%，单日市值蒸发5890亿美元。', '英伟达和美国股市的关系是英伟达创历史纪录美国股市,创下美国股市历史上最高纪录。', '深度求索（DeepSeek）和美股 AI、芯片股的关系是深度求索（DeepSeek）被认为是重要因素美股 AI、芯片股,深度求索（DeepSeek）被认为是美股AI、芯片股波动的重要因素之一。']

# print(asyncio.run(main(mock_data)))

from deeprag.workflow.vector_query_to_vector_db import query_vector_db_by_vector
import asyncio


async def main(mock_data):
    response = await query_vector_db_by_vector(mock_data, "test")
    return response


a = asyncio.run(main("AI美股"))
print(a)
# print(type(a))
# print(dir(a))
# print(a[0])
# context = [item["entity"]["text"] for item in a[0]]
# print(context)


# search_params = {
#     'params': {'drop_ratio_search': 0.2},
# }


# import asyncio
# async def main():
#     client = await create_or_use_hybrid_search_milvus_client_collection()

#     res = client.search(
#         collection_name='test',
#         collection_name='test',
#         data=['AI美股'],
#         anns_field='sparse',
#         limit=3,
#         search_params=search_params
#     )
#     return res
# print(asyncio.run(main()))
