from deeprag.db.dao.flatten_entity_relation.flatten_entity_realtion_dao import (
    FlattenEntityRelationDAO,
)
import uuid
from prisma.models import flatten_entity_relation


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
        head_entity_list: list[str],
        tail_entity_list: list[str],
        relation_description_list: list[str],
        merged_graph_data_id_list: list[str],
        community_id_list: list[str] | None = None,
    ) -> int:
        id_list = [str(uuid.uuid4()) for _ in range(len(community_id_list))]
        stored_flatten_entity_relation_count = (
            await self.dao.batch_create_flatten_entity_relation(
                id_list,
                head_entity_list,
                tail_entity_list,
                relation_description_list,
                merged_graph_data_id_list,
                community_id_list,
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
