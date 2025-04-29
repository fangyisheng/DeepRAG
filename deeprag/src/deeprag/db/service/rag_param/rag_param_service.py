from deeprag.db.dao.rag_param.rag_param_dao import RagParamDAO
from prisma.models import rag_param
import uuid


class RagParamService:
    def __init__(self):
        self.dao = RagParamDAO()

    async def create_rag_param(
        self, grounds_for_response: str, message_id: str
    ) -> rag_param:
        id = str(uuid.uuid4())
        strored_rag_param = await self.dao.create_rag_param(
            id=id, grounds_for_response=grounds_for_response, message_id=message_id
        )
        return strored_rag_param

    async def get_rag_param_by_message_id(self, message_id: str) -> rag_param:
        found_rag_param = await self.dao.get_rag_param_by_message_id(message_id)

        return found_rag_param
