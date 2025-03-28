from deeprag.agent.index.extract_entity_relationship_graph import (
    extract_entity_relationship_agent,
)
import asyncio
from deeprag.workflow.data_model import BatchTextChunkGenerateGraphsResponse


async def batch_text_chunk_generate_graphs_process(
    chunked_text_array: list,
) -> BatchTextChunkGenerateGraphsResponse:
    """_summary_

    Args:
        chunked_text_array (list): 文本分块的列表

    Returns:
        list[dict]: 每个文本分块对应的图结构的列表
    """
    tasks = [
        extract_entity_relationship_agent(text_chunk)
        for text_chunk in chunked_text_array
    ]
    results = await asyncio.gather(*tasks)
    return results
