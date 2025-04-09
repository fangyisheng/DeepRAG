from deeprag.workflow.data_model import 

async def merged_graph_data_to_flattend_entity_relation_process(
    merged_graph_data: MergedGraphData,
) -> CompleteGraphData:
    flattend_entity_relation_list = []
    for relation in merged_graph_data.relations:
        head_entity = next(entity.text for entity in merged_graph_data.entities if relation.head == entity.id)
        end_entity = next(entity.text for entity in merged_graph_data.entities if relation.end == entity.id)
        relation_description = relation.relation_description
        flattend_entity_relation_list.append(
            {"head_entity": head_entity, "tail_entity": end_entity, "relation": relation_description}
        )
    
    return flattend_esntity_relation_list