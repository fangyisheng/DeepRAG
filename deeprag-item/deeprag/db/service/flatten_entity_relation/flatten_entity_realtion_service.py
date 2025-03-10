from deeprag.db.dao.flatten_entity_relation.flatten_entity_realtion_dao import FlattenEntityRelationDAO


class FlattenEntityRelationService:
    def __init__(self):
        self.dao = FlattenEntityRelationDAO()

    async def get_flatten_entity_relation_by_community_id(self, community_id:str):
        flatten_entity_relation = await self.dao.get_flatten_entity_relation_by_community_id(community_id)
        return flatten_entity_relation.__dict__
    
    async def get_flatten_entity_relation_by_id(self, id:str):
        flatten_entity_relation = await self.dao.get_flatten_entity_relation_by_id(id)
        return flatten_entity_relation.__dict__

    