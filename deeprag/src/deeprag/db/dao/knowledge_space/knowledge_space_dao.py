from prisma import Prisma
from dotenv import load_dotenv
from prisma.models import knowledge_space
from deeprag.db.data_model import UpdateKnowledgeSpace

load_dotenv()


class KnowledgeSpaceDAO:
    def __init__(self):
        self.db = Prisma()

    async def create_knowledge_space(
        self, id: str, user_id: str, knowledge_space_name: str
    ) -> knowledge_space:
        await self.db.connect()
        stored_knowledge_space = await self.db.knowledge_space.create(
            data={
                "user_id": user_id,
                "id": id,
                "knowledge_space_name": knowledge_space_name,
            }
        )
        await self.db.disconnect()
        return stored_knowledge_space

    async def delete_knowledge_space(self, id: str) -> knowledge_space:
        await self.db.connect()
        deleted_knowledge_space = await self.db.knowledge_space.delete(where={"id": id})
        await self.db.connect()
        return deleted_knowledge_space

    async def get_knowledge_space_by_id(self, id: str) -> knowledge_space:
        await self.db.connect()
        found_knowledge_space = await self.db.knowledge_space.find_unique(
            where={"id": id}
        )
        await self.db.connect()
        return found_knowledge_space

    async def update_knowledge_space(
        self, id: str, data: UpdateKnowledgeSpace
    ) -> knowledge_space:
        await self.db.connect()
        updated_knowledge_space = await self.db.knowledge_space.update(
            where={"id": id}, data=data
        )
        await self.db.disconnect()
        return updated_knowledge_space

    async def get_knowledge_space_by_knowledge_space_name(
        self, knowledge_space_name: str
    ) -> list[knowledge_space]:
        """
        对知识库空间进行知识库名字的精确检索
        """
        await self.db.connect()
        found_knowledge_space = await self.db.knowledge_space.find_many(
            where={"knowledge_space_title": knowledge_space_name}
        )
        await self.db.disconnect()
        return found_knowledge_space

    async def search_knowledge_space_by_knowledge_space_name(
        self, knowledge_space_name: str
    ) -> list[knowledge_space]:
        """
        对知识库空间进行知识库名字的模糊检索
        """
        await self.db.connect()
        found_knowledge_space = await self.db.knowledge_space.find_many(
            where={"knowledge_space_title": {"contains": knowledge_space_name}}
        )
        await self.db.disconnect()
        return found_knowledge_space
