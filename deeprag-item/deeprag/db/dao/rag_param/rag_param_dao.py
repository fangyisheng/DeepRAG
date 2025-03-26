from prisma import Prisma
from dotenv import load_dotenv

load_dotenv()


class RagParamDAO:
    def __init__(self):
        self.db = Prisma()

    async def create_rag_param(
        self, id: str, grounds_for_response: str, message_id: str
    ):
        await self.db.connect()
        stored_rag_param = await self.db.rag_param.create(
            data={
                "id": id,
                "grounds_for_response": grounds_for_response,
                "message_id": message_id,
            }
        )
        await self.db.disconnect()
        return stored_rag_param.model_dump()

    async def get_rag_param_by_id(self, id: str):
        await self.db.connect()
        found_rag_param = await self.db.rag_param.find_unique(where={"id": id})
        await self.db.disconnect()
        return found_rag_param.model_dump()

    async def get_rag_param_by_message_id(self, message_id: str):
        await self.db.connect()
        found_rag_param = await self.db.rag_param.find_unique(
            where={"message_id": message_id}
        )
        await self.db.disconnect()
        return found_rag_param.model_dump()
