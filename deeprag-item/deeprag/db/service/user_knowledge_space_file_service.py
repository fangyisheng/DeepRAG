from deeprag.db.dao.user_knowledge_space_file_dao import UserKnowledgeSpaceFileDAO


class UserKnowledgeSpaceFileService:
    def __init__(self):
        self.dao = UserKnowledgeSpaceFileDAO()

    async def get_complete_knowledge_scope_structure(self) -> list[dict]:
        """
        获取完整的知识空间结构
        """
        complete_knowledge_scope_structure = (
            await self.dao.get_complete_knowledge_scope_structure()
        )
        return [
            knowledge_scope_structure.model_dump()
            for knowledge_scope_structure in complete_knowledge_scope_structure
        ]
