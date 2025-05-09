from prisma import Prisma
from prisma.models import flatten_entity_relation
from dotenv import load_dotenv
from deeprag.workflow.data_model import FlattenEntityRelation

load_dotenv()


class FlattenEntityRelationDAO:
    def __init__(self):
        pass

    async def create_flatten_entity_relation(
        self,
        id: str,
        head_entity: str,
        tail_entity: str,
        relation: str,
        merged_graph_data_id: str,
        community_id: str,
    ) -> flatten_entity_relation:
        async with Prisma() as db:
            stored_flatten_entity_relation = await db.flatten_entity_relation.create(
                data={
                    "id": id,
                    "head_entity": head_entity,
                    "tail_entity": tail_entity,
                    "relation": relation,
                    "merged_graph_data_id": merged_graph_data_id,
                    "community_id": community_id,
                }
            )

        return stored_flatten_entity_relation

    async def batch_create_flatten_entity_relation(
        self,
        flatten_entity_relations: list[FlattenEntityRelation],
    ) -> int:
        async with Prisma() as db:
            stored_flatten_entity_relation_count = (
                await db.flatten_entity_relation.create_many(
                    data=[
                        flatten_entity_relation.model_dump()
                        for flatten_entity_relation in flatten_entity_relations
                    ]
                )
            )

        return stored_flatten_entity_relation_count

    async def get_flatten_entity_relation_by_id(
        self, id: str
    ) -> flatten_entity_relation:
        async with Prisma() as db:
            found_flatten_entity_relation = (
                await db.flatten_entity_relation.find_unique(where={"id": id})
            )

        return found_flatten_entity_relation

    async def get_flatten_entity_relation_by_community_id(
        self, community_id: str
    ) -> list[flatten_entity_relation]:
        async with Prisma() as db:
            found_flatten_entity_relation_list = (
                await db.flatten_entity_relation.find_many(
                    where={"community_id": community_id}
                )
            )

        return found_flatten_entity_relation_list
