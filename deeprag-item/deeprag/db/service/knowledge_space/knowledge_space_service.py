from deeprag.db.dao.knowledge_space.knowledge_space_dao import KnowledgeSpaceDAO
import json
import uuid


class KnowledgeSpaceService:
    def __init__(self):
        self.dao = KnowledgeSpaceDAO()

    async def create_knowledge_space(self, knowledge_space_title: str) -> dict:
        id = str(uuid.uuid4())
        knowledge_space_id = str(uuid.uuid4())
        created_knowledge_space = await self.dao.create_knowledge_space(
            id, knowledge_space_id, knowledge_space_title
        )
        return created_knowledge_space.model_dump()

    async def delete_knowledge_space(self, id: str) -> dict:
        deleted_knowledge_space = await self.dao.delete_knowledge_space(id)
        return deleted_knowledge_space.model_dump()

    async def get_knowledge_space_by_id(self, id: str) -> dict:
        found_knowledge_space = await self.dao.get_knowledge_space_by_id(id)

        return found_knowledge_space.model_dump()

    async def update_knowledge_space(self, id: str, data: dict):
        updated_knowledge_space = await self.dao.knowledge_space.update(id, data)

        return updated_knowledge_space.model_dump()
