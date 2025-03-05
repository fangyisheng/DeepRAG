from deeprag.db.dao.knowledge_space.knowledge_space_dao import KnowledgeSpaceDAO
import json
import uuid

class KnowledgeSpaceService:
    def __init__(self):
        self.dao = KnowledgeSpaceDAO()
    
    async def create_knowledge_space_service(self,knowledge_space_title: str):
        id = str(uuid.uuid4())
        knowledge_space_id = str(uuid.uuid4())
        knowledge_space = await self.dao.create_knowledge_space(
            id,
            knowledge_space_id,
            knowledge_space_title
        )
        return knowledge_space.__dict__
    
    async def delete_knowledge_space_service(self, knowledge_space_id: str):
        knowledge_space =  await self.dao.delete_knowledge_space(
            knowledge_space_id
        )
        return knowledge_space.__dict__
    
    async def get_knowledge_space_by_id(self, id: str):
        
        knowledge_space = await self.dao.get_knowledge_space_by_id(id)
        
        return knowledge_space.__dict__
    
    async def update_knowledge_space(self, id: str, data: dict):

        knowledge_space = await self.dao.knowledge_space.update(
         id,data
        )

        return knowledge_space.__dict__
    