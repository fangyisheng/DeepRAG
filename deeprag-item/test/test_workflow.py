from deeprag.text_extract_and_clean import process_text
from deeprag.text_chunk_based_by_token import TextSplitter
from deeprag.agent.index.extract_entity_relationship_graph import extract_entity_relationship_agent
from deeprag.agent.index.graph_storage_to_html_with_no_leiden import store_graph_data_to_html
import asyncio
from loguru import logger
import time

async def main():
     cleaned_text = await process_text("/home/easonfang/DeepRAG/deeprag-item/deeprag/knowledge_file/test.txt")
     logger.info("文本预清洗完成")
    #  logger.info(f"这是清洗好的文本：{cleaned_text}")
     logger.info(f"这是清洗好的文本的字符串长度:{len(cleaned_text)}")
     splitter = TextSplitter()
     chunks = await splitter.split_text_by_token(text=cleaned_text)
     logger.info("文本切分完成")
    
     logger.info(f"这是切分好的文本分块列表：{chunks}")
    #  tasks = [extract_entity_relationship_agent(chunk) for chunk in chunks]
    #  start_time = time.perf_counter()
    #  results = await asyncio.gather(*tasks)
    #  end_time = time.perf_counter()
    #  print(f"多并发执行时间：{end_time - start_time}")
     start_time = time.perf_counter()
     results = await extract_entity_relationship_agent(chunks[2])
     end_time = time.perf_counter()
     print(f"单并发执行时间：{end_time - start_time}")

    
     
    #  another_tasks = [store_graph_data_to_html(graph) for graph in results]
    #  new_results = await asyncio.gather(*another_tasks)
    

asyncio.run(main())

