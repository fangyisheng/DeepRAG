from deeprag.agent.index.extract_entity_relationship_graph import extract_entity_relationship_agent
import asyncio

async def batch_text_chunk_generate_graphs_process(chunked_text_array:list):
    tasks = [extract_entity_relationship_agent(text_chunk) for text_chunk in chunked_text_array]
    results = await asyncio.gather(*tasks)
    return results



    