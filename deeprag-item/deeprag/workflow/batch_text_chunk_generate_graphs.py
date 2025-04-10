from deeprag.agent.index.extract_entity_relationship_graph import (
    extract_entity_relationship_agent,
)
import asyncio
from deeprag.workflow.data_model import (
    BatchTextChunkGenerateGraphsResponse,
    ChunkedTextUnit,
)


async def batch_text_chunk_generate_graphs_process(
    chunked_text_array: ChunkedTextUnit,
) -> BatchTextChunkGenerateGraphsResponse:
    """_summary_

    Args:
        chunked_text_array (list): 文本分块的列表

    Returns:
        list[dict]: 每个文本分块对应的图结构的列表
    """
    tasks = [
        extract_entity_relationship_agent(text_chunk)
        for text_chunk in chunked_text_array.root
    ]
    results = await asyncio.gather(*tasks)
    return BatchTextChunkGenerateGraphsResponse(root=results)


# 进行测试
import asyncio

chunked_text_array = ChunkedTextUnit(root=[""])
