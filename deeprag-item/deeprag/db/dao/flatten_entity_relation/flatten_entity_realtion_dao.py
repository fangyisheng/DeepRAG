from prisma import Prisma
from prisma.models import flatten_entity_relation
from dotenv import load_dotenv

load_dotenv()


class FlattenEntityRelationDAO:
    def __init__(self):
        self.db = Prisma()

    async def create_flatten_entity_relation(
        self,
        id: str,
        head_entity: str,
        tail_entity: str,
        relation: str,
        merged_graph_data_id: str,
        community_id: str,
    ) -> flatten_entity_relation:
        await self.db.connect()
        stored_flatten_entity_relation = await self.db.flatten_entity_relation.create(
            data={
                "id": id,
                "head_entity": head_entity,
                "tail_entity": tail_entity,
                "relation": relation,
                "merged_graph_data_id": merged_graph_data_id,
                "community_id": community_id,
            }
        )
        await self.db.disconnect()
        return stored_flatten_entity_relation

    async def batch_create_flatten_entity_relation(
        self,
        id_list: list[str],
        head_entity_list: list[str],
        tail_entity_list: list[str],
        relation_description_list: list[str],
        merged_graph_data_id_list: list[str],
        community_id_list: list[str] | None = None,
    ) -> int:
        await self.db.connect()
        stored_flatten_entity_relation_count = await self.db.flatten_entity_relation.create_many(
            data=[
                {
                    "id": id,
                    "head_entity": head_entity,
                    "tail_entity": tail_entity,
                    "relation_description": relation_description,
                    "merged_graph_data_id": merged_graph_data_id,
                    "community_id": community_id,
                }
                for id, head_entity, tail_entity, relation_description, merged_graph_data_id, community_id in zip(
                    id_list,
                    head_entity_list,
                    tail_entity_list,
                    relation_description_list,
                    merged_graph_data_id_list,
                    community_id_list,
                )
            ]
        )
        return stored_flatten_entity_relation_count

    async def get_flatten_entity_relation_by_id(
        self, id: str
    ) -> flatten_entity_relation:
        await self.db.connect()
        found_flatten_entity_relation = (
            await self.db.flatten_entity_relation.find_unique(where={"id": id})
        )
        await self.db.disconnect()
        return found_flatten_entity_relation

    async def get_flatten_entity_relation_by_community_id(
        self, community_id: str
    ) -> list[flatten_entity_relation]:
        await self.db.connect()
        found_flatten_entity_relation_list = (
            await self.db.flatten_entity_relation.find_many(
                where={"community_id": community_id}
            )
        )
        await self.db.disconnect()
        return found_flatten_entity_relation_list
