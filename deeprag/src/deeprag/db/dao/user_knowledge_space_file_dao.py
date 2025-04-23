from prisma import Prisma
from prisma.models import user
from deeprag.workflow.data_model import KnowledgeScopeLocator, KnowledgeScopeRealName


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
        found_user_name = await self.db.user.find_unique(
            where={
                "id": knowledge_scope_locator.user_id,
            }
        )
        found_knowledge_space_name = await self.db.knowledge_space.find_unique(
            where={
                "id": knowledge_scope_locator.knowledge_space_id,
            },
        )

        found_file_name = await self.db.file.find_unique(
            where={
                "id": knowledge_scope_locator.file_id,
            },
        )

        await self.db.disconnect()
        return KnowledgeScopeRealName(
            user_name=found_user_name.user_name,
            knowledge_space_name=found_knowledge_space_name.knowledge_space_name,
            file_name=found_file_name.doc_title,
        )
