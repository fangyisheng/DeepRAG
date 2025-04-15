

from deeprag.workflow.data_model import CompleteGraphData

async def batch_flatten_entity_relation_func(
    entity_relationship: CompleteGraphData,
) -> list[EntityRelation]: