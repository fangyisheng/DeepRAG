from deeprag.db.dao.rag_param.rag_param_dao import RagParamDAO

class RagParamService:
    def __init__(self):
        self.dao = RagParamDAO()

    async def get_rag_param_by_message_id(self,message_id: str):
        rag_param = await self.dao.get_rag_param_by_message_id(message_id)

        return rag_param.__dict__
