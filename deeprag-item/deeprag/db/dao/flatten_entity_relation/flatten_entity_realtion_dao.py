from prisma import Prisma

class FlattenEntityRelationDAO:
    def __init__(self):
        self.db =  Prisma()

    async def create_flatten_entity_relation(self, id:str, head_entity:str,tail_entity:str, relation:str, merged_graph_data_id:str, community_id:str):
        await self.db.connect()
        flatten_entity_relation = await self.db.flatten_entity_relation.create(
            data = {
                "id":id,
                "head_entity":head_entity,
                "tail_entity":tail_entity,
                "relation":relation,
                "merged_graph_data_id":merged_graph_data_id,
                "community_id":community_id
            }
        )
        await self.db.disconnect()
        return flatten_entity_relation
    
    async def get_flatten_entity_relation_by_id(self,id:str):
        await self.db.connect()
        flatten_entity_relation = await self.db.flatten_entity_relation.find_unique(
            where = {"id":id}
        )
        await self.db.disconnect()
        return flatten_entity_relation