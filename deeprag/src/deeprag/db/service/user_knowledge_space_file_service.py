from deeprag.db.dao.user_knowledge_space_file_dao import UserKnowledgeSpaceFileDAO
from deeprag.workflow.data_model import KnowledgeScopeLocator
from deeprag.workflow.data_model import KnowledgeScopeRealName
from prisma.models import user


class UserKnowledgeSpaceFileService:
    def __init__(self):
        self.dao = UserKnowledgeSpaceFileDAO()

    async def get_all_knowledge_scope_structure(self) -> list[dict]:
        """
        获取所有的知识空间结构
        """
        complete_knowledge_scope_structure = (
            await self.dao.get_all_knowledge_scope_structure()
        )
        return [
            knowledge_scope_structure.model_dump()
            for knowledge_scope_structure in complete_knowledge_scope_structure
        ]

    async def get_knowledge_scope_real_name_by_id(
        self, knowledge_scope_locator: KnowledgeScopeLocator
    ) -> KnowledgeScopeRealName:
        """
        根据知识空间id获取知识空间的真实名字
        """
        knowledge_scope_real_name: KnowledgeScopeRealName = (
            await self.dao.get_knowledge_scope_real_name_by_id(knowledge_scope_locator)
        )
        return knowledge_scope_real_name
