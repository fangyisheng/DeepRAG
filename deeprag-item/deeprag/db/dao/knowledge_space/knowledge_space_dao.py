from prisma import Prisma
from dotenv import load_dotenv

load_dotenv()


class KnowledgeSpaceDAO:
    def __init__(self):
        self.db = Prisma()

    async def create_knowledge_space(
        self, id: str, user_id: str, knowledge_space_title: str
    ):
        await self.db.connect()
        stored_knowledge_space = await self.db.knowledge_space.create(
            data={
                "user_id": user_id,
                "id": id,
                "knowledge_space_title": knowledge_space_title,
            }
        )
        await self.db.disconnect()
        return stored_knowledge_space.model_dump()

    async def delete_knowledge_space(self, id: str):
        await self.db.connect()
        deleted_knowledge_space = await self.db.knowledge_space.delete(where={"id": id})
        await self.db.connect()
        return deleted_knowledge_space.model_dump()

    async def get_knowledge_space_by_id(self, id: str):
        await self.db.connect()
        found_knowledge_space = await self.db.knowledge_space.find_unique(
            where={"id": id}
        )
        await self.db.connect()
        return found_knowledge_space.model_dump()

    async def update_knowledge_space(self, id: str, data: dict):
        await self.db.connect()
        updated_knowledge_space = await self.db.knowledge_space.update(
            where={"id": id}, data=data
        )
        await self.db.disconnect()
        return updated_knowledge_space.model_dump()
