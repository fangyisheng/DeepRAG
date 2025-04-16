from deeprag.db.dao.flatten_entity_relation.flatten_entity_realtion_dao import (
    FlattenEntityRelationDAO,
)
import uuid
from prisma.models import flatten_entity_relation
from deeprag.workflow.data_model import (
    FlattenEntityRelation,
)


class FlattenEntityRelationService:
    def __init__(self):
        self.dao = FlattenEntityRelationDAO()

    async def create_flatten_entity_relation(
        self,
        head_entity: str,
        tail_entity: str,
        relation: str,
        merged_graph_data_id: str,
        community_id: str,
    ) -> flatten_entity_relation:
        id = str(uuid.uuid4())
        stored_flatten_entity_relation = await self.dao.create_flatten_entity_relation(
            id, head_entity, tail_entity, relation, merged_graph_data_id, community_id
        )
        return stored_flatten_entity_relation

    async def batch_create_flatten_entity_relation(
        self,
        flatten_entity_relation_list: list[FlattenEntityRelation],
    ) -> int:
        stored_flatten_entity_relation_count = (
            await self.dao.batch_create_flatten_entity_relation(
                flatten_entity_relation_list
            )
        )
        return stored_flatten_entity_relation_count

    async def get_flatten_entity_relation_by_community_id(
        self, community_id: str
    ) -> list:
        found_flatten_entity_relation_list = (
            await self.dao.get_flatten_entity_relation_by_community_id(community_id)
        )
        return found_flatten_entity_relation_list

    async def get_flatten_entity_relation_by_id(self, id: str):
        found_flatten_entity_relation = (
            await self.dao.get_flatten_entity_relation_by_id(id)
        )
        return found_flatten_entity_relation.model_dump()
