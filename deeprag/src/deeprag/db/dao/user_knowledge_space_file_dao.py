from prisma import Prisma
from prisma.models import user
from deeprag.workflow.data_model import KnowledgeScopeLocator, KnowledgeScopeRealName
from dotenv import load_dotenv


load_dotenv()


class UserKnowledgeSpaceFileDAO:
    def __init__(self):
        self.db = Prisma()

    async def get_all_knowledge_scope_structure(self) -> list[user]:
        await self.db.connect()
        all_knowledge_scope_structure = await self.db.user.find_many(
            include={
                "knowledge_spaces": {
                    "include": {
                        "files": True,
                    }
                },
            },
        )
        await self.db.disconnect()
        return all_knowledge_scope_structure

    async def get_knowledge_scope_real_name_by_id(
        self, knowledge_scope_locator: KnowledgeScopeLocator
    ) -> KnowledgeScopeRealName:
        await self.db.connect()
        found_user = await self.db.user.find_unique(
            where={
                "id": knowledge_scope_locator.user_id,
            }
        )
        found_knowledge_space = await self.db.knowledge_space.find_unique(
            where={
                "id": knowledge_scope_locator.knowledge_space_id,
            },
        )

        found_file = await self.db.file.find_unique(
            where={
                "id": knowledge_scope_locator.file_id,
            },
        )

        await self.db.disconnect()
        return KnowledgeScopeRealName(
            user_name=found_user.user_name,
            knowledge_space_name=found_knowledge_space.knowledge_space_name,
            file_name=found_file.doc_title,
        )


# 写一点测试代码

# import asyncio

# user_knowledge_space_file_dao = UserKnowledgeSpaceFileDAO()


# async def main():
#     result = await user_knowledge_space_file_dao.get_knowledge_scope_real_name_by_id(
#         knowledge_scope_locator=KnowledgeScopeLocator(
#             user_id="67f54e07-03aa-4319-9fcd-93034e8e990c",
#             knowledge_space_id="a1fe02fe-76be-4bb6-9498-aa9cd86e8b8f",
#             file_id="0da4cf66-ab9d-4378-a54d-c87ea0b36651",
#         )
#     )
#     return result


# print(asyncio.run(main()))
