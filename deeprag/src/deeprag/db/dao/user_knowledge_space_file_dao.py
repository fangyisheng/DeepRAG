from prisma import Prisma
from prisma.models import user
from deeprag.workflow.data_model import KnowledgeScopeLocator


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

    async def get_knowledge_scope_by_id(
        self, knowledge_scope_locator: KnowledgeScopeLocator
    ):
        await self.db.connect()
        found_knowledge_scope = await self.db.user.find_unique(
            where={
                "id": knowledge_scope_locator.user_id,
                "knowledge_spaces": {
                    "is": {
                        "id": knowledge_scope_locator.knowledge_space_id,
                        "files": {
                            "is": {
                                "id": knowledge_scope_locator.file_id,
                            }
                        },
                    }
                },
            },
            include={
                "knowledge_spaces": {
                    "include": {
                        "files": True,
                    }
                },
            },
        )

        await self.db.disconnect()
        return found_knowledge_scope
