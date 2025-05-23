from deeprag.workflow.text_extract_and_clean import process_text
from deeprag.workflow.text_chunk_process import TextSplitter
from deeprag.agent.index.extract_entity_relationship_graph import (
    extract_entity_relationship_agent,
)
from deeprag.workflow.batch_text_chunk_generate_graphs import (
    batch_text_chunk_generate_graphs_process,
)
from deeprag.workflow.graph_storage_to_html_with_no_leiden import (
    store_graph_data_to_html_with_no_leiden,
)
from deeprag.workflow.merge_sub_graph import merge_sub_entity_relationship_graph
from deeprag.workflow.graph_description_enrichment import describe_graph


import asyncio
from loguru import logger
import time


async def main():
    cleaned_text = await process_text(
        "/home/easonfang/DeepRAG/deeprag-item/deeprag/knowledge_file/test2.txt"
    )
    logger.info("文本预清洗完成")
    #  logger.info(f"这是清洗好的文本：{cleaned_text}")
    logger.info(f"这是清洗好的文本的字符串长度:{len(cleaned_text)}")
    splitter = TextSplitter()
    chunks = await splitter.split_text_by_token(text=cleaned_text)
    logger.info("文本切分完成")
    logger.info(f"这是切分好的文本分块列表：{chunks}")
    graphs = await batch_text_chunk_generate_graphs_process(chunks)
    logger.info(f"这是根据文本分块一起提取的图结构：{graphs}")
    merged_graphs = await merge_sub_entity_relationship_graph(graphs)
    logger.info(f"这是合并好的完整图结构：{merged_graphs}")
    relation_description = await describe_graph(merged_graphs)
    logger.info(f"这是加工后的关系列表：{relation_description}")


#  tasks = [extract_entity_relationship_agent(cshunk) for chunk in chunks]
#  start_time = time.perf_counter()
#  results = await asyncio.gather(*tasks)
#  end_time = time.perf_counter()
#  print(f"多并发执行时间：{end_time - start_time}")
#  start_time = time.perf_counter()
#  results = await extract_entity_relationship_agent(chunks[2])
#  end_time = time.perf_counter()
#  print(f"单并发执行时间：{end_time - start_time}")


#  another_tasks = [store_graph_data_to_html(graph) for graph in results]
#  new_results = await asyncio.gather(*another_tasks)


asyncio.run(main())
