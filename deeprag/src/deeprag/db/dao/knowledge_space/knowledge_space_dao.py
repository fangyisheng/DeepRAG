from prisma import Prisma
from dotenv import load_dotenv
from prisma.models import knowledge_space
from deeprag.db.data_model import UpdateKnowledgeSpace

load_dotenv()


class KnowledgeSpaceDAO:
    def __init__(self):
        pass

    async def create_knowledge_space(
        self, id: str, user_id: str, knowledge_space_name: str
    ) -> knowledge_space:
        async with Prisma() as db:
            stored_knowledge_space = await db.knowledge_space.create(
                data={
                    "user_id": user_id,
                    "id": id,
                    "knowledge_space_name": knowledge_space_name,
                }
            )

        return stored_knowledge_space

    async def delete_knowledge_space(self, id: str) -> knowledge_space:
        async with Prisma() as db:
            deleted_knowledge_space = await db.knowledge_space.delete(where={"id": id})
        await db.connect()
        return deleted_knowledge_space

    async def get_knowledge_space_by_id(self, id: str) -> knowledge_space:
        async with Prisma() as db:
            found_knowledge_space = await db.knowledge_space.find_unique(
                where={"id": id}
            )
        await db.connect()
        return found_knowledge_space

    async def batch_get_knowledge_space_by_id_list(
        self, id_list: list[str]
    ) -> list[knowledge_space]:
        async with Prisma() as db:
            found_knowledge_space_list = await db.knowledge_space.find_many(
                where={"id": {"in": id_list}}
            )

        return found_knowledge_space_list

    async def update_knowledge_space(
        self, id: str, data: UpdateKnowledgeSpace
    ) -> knowledge_space:
        async with Prisma() as db:
            updated_knowledge_space = await db.knowledge_space.update(
                where={"id": id}, data=data
            )

        return updated_knowledge_space

    async def get_knowledge_space_by_knowledge_space_name(
        self, knowledge_space_name: str
    ) -> list[knowledge_space]:
        """
        对知识库空间进行知识库名字的精确检索
        """
        async with Prisma() as db:
            found_knowledge_space = await db.knowledge_space.find_many(
                where={"knowledge_space_title": knowledge_space_name}
            )

        return found_knowledge_space

    async def search_knowledge_space_by_knowledge_space_name(
        self, knowledge_space_name: str
    ) -> list[knowledge_space]:
        """
        对知识库空间进行知识库名字的模糊检索
        """
        async with Prisma() as db:
            found_knowledge_space = await db.knowledge_space.find_many(
                where={"knowledge_space_title": {"contains": knowledge_space_name}}
            )

        return found_knowledge_space
