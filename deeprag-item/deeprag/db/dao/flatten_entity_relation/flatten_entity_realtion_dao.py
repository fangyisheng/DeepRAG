from prisma import Prisma
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
    ):
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
        return stored_flatten_entity_relation.model_dump()

    async def get_flatten_entity_relation_by_id(self, id: str):
        await self.db.connect()
        found_flatten_entity_relation = (
            await self.db.flatten_entity_relation.find_unique(where={"id": id})
        )
        await self.db.disconnect()
        return found_flatten_entity_relation.model_dump()

    async def get_flatten_entity_relation_by_community_id(self, community_id: str):
        await self.db.connect()
        found_flatten_entity_relation_list = (
            await self.db.flatten_entity_relation.find_many(
                where={"community_id": community_id}
            )
        )
        await self.db.disconnect()
        return found_flatten_entity_relation_list
