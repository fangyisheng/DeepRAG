from deeprag.workflow.data_model import GraphDescriptionResponse


async def batch_flatten_entity_relation_func(
    entity_relationship: GraphDescriptionResponse, s
) -> list[EntityRelation]:
    flatten_entity_relation_list = []
    for relation in entity_relationship.relations:
        head_entity = next(
            entity.text
            for entity in entity_relationship.entities
            if relation.head == entity.id
        )
        end_entity = next(
            entity.text
            for entity in entity_relationship.entities
            if relation.end == entity.id
        )
        relation_description = relation.description
        id = relation.id
        flatten_entity_relation_list.append(
            {
                "id": id,
                "head_entity": head_entity,
                "tail_entity": end_entity,
                "relation_description": relation_description,
            }
        )
