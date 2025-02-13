from deeprag.agent.index.extract_entity_relationship_graph import extract_entity_relationship_agent
import asyncio
import time

async def main():
    start_time = time.perf_counter()
    result =  await extract_entity_relationship_agent("我是医生")
    end_time = time.perf_counter
    return result

print(asyncio.run(main()))