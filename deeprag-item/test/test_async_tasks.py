from deeprag.agent.index.extract_entity_relationship_graph import extract_entity_relationship_agent
import asyncio
import time
from loguru import logger


async def main():
    start_time = time.perf_counter()
    tasks = [extract_entity_relationship_agent(task) for task in ["我是医生","我是女儿","我来自阿里云"]]
    result =  await asyncio.gather(*tasks)
    end_time = time.perf_counter()
    logger.info(f"多并发时间为：{end_time - start_time}")


 

