from deeprag.db.dao.knowledge_space.knowledge_space_dao import KnowledgeSpaceDAO
import json
import uuid
from prisma.models import knowledge_space


class KnowledgeSpaceService:
    def __init__(self):
        self.dao = KnowledgeSpaceDAO()

    async def create_knowledge_space(
        self, user_id: str, knowledge_space_name: str
    ) -> knowledge_space:
        id = str(uuid.uuid4())
        created_knowledge_space = await self.dao.create_knowledge_space(
            id, user_id, knowledge_space_name
        )
        return created_knowledge_space

    async def delete_knowledge_space(self, id: str) -> knowledge_space:
        deleted_knowledge_space = await self.dao.delete_knowledge_space(id)
        return deleted_knowledge_space

    async def get_knowledge_space_by_id(self, id: str) -> knowledge_space:
        found_knowledge_space = await self.dao.get_knowledge_space_by_id(id)

        return found_knowledge_space

    async def get_user_id_by_knowledge_space_id(self, id: str) -> str:
        found_knowledge_space = await self.dao.get_knowledge_space_by_id(id)
        return found_knowledge_space.user_id

    async def batch_get_knowledge_space_by_id_list(
        self, id_list: list[str]
    ) -> list[knowledge_space]:
        found_knowledge_space_list = (
            await self.dao.batch_get_knowledge_space_by_id_list(id_list)
        )
        return found_knowledge_space_list

    async def update_knowledge_space(self, id: str, data: dict) -> knowledge_space:
        updated_knowledge_space = await self.dao.update_knowledge_space(id, data)

        return updated_knowledge_space

    async def get_knowledge_space_by_knowledge_space_name(
        self, knowledge_space_name: str
    ) -> list[knowledge_space]:
        found_knowledge_space = (
            await self.dao.get_knowledge_space_by_knowledge_space_name(
                knowledge_space_name
            )
        )

        return found_knowledge_space

    async def search_knowledge_space_by_knowledge_space_name(
        self, knowledge_space_name: str
    ) -> list[dict]:
        found_knowledge_space = (
            await self.dao.search_knowledge_space_by_knowledge_space_name(
                knowledge_space_name
            )
        )

        return [
            knowledge_space.model_dump() for knowledge_space in found_knowledge_space
        ]
