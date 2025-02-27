from deeprag.db.dao.knowledge_space.knowledge_space_dao import KnowledgeSpaceDAO
import json
import uuid

class KnowledgeSpaceService:
    def __init__(self):
        self.dao = KnowledgeSpaceDAO()
    
    async def create_knowledge_space_dao(self,knowledge_space_title: str):
        id = str(uuid.uuid4())
        knowledge_space_id = str(uuid.uuid4())
        knowledge_space = await self.dao.create_knowledge_space(
            id,
            knowledge_space_id,
            knowledge_space_title
        )
        return knowledge_space.__dict__