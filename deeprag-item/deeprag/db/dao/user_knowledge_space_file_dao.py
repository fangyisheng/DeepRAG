from prisma import Prisma
from prisma.models import user


class UserKnowledgeSpaceFileDAO:
    def __init__(self):
        self.db = Prisma()

    async def get_complete_knowledge_scope_structure(self) -> list[user]:
        complete_knowledge_scope_structure = await self.db.user.find_many(
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
        return complete_knowledge_scope_structure
