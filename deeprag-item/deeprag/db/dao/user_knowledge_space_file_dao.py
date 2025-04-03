from prisma import Prisma
from prisma.models import user
from deeprag.workflow.data_model import KnowledgeScopeLocator


class UserKnowledgeSpaceFileDAO:
    def __init__(self):
        self.db = Prisma()

    async def get_all_knowledge_scope_structure(self) -> list[user]:
        await self.db.connect()
        all_knowledge_scope_structure = await self.db.user.find_many(
            select={
                "user_name": True,
                "knowledge_spaces": {
                    "select": {
                        "knowledge_space_title": True,
                        "files": {
                            "select": {
                                "doc_title": True,
                            }
                        },
                    }
                },
            }
        )
        await self.db.disconnect()
        return all_knowledge_scope_structure

    async def get_knowledge_scope_by_id(
        self, knowledge_scope_locator: KnowledgeScopeLocator
    ):
        await self.db.connect()
        found_knowledge_scope = await self.db.user.find_unique(
            select = 
        )

        await self.db.disconnect()
