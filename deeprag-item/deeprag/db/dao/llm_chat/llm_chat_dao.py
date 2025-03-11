from prisma import Prisma


class LLMChatDAO:
    def __init__(self):
        self.db = Prisma()

    async def create_message(
        self,
        id: str,
        user_id: str,
        user_prompt: str,
        user_context: str,
        llm_answer: str,
        message_start_time: str,
        message_end_time: str,
        message_duration_time: str,
        session_id: str,
        cost_tokens: str,
    ):
        await self.db.connect()
        message = await self.db.llm_chat.create(
            data={
                "id": id,
                "user_id": user_id,
                "user_prompt": user_prompt,
                "user_context": user_context,
                "llm_answer": llm_answer,
                "message_start_time": message_start_time,
                "message_end_time": message_end_time,
                "message_duration_time": message_duration_time,
                "session_id": session_id,
                "cost_tokens": cost_tokens,
            }
        )
        await self.db.disconnect()
        return message

    async def get_message_by_id(self, id: str):
        await self.db.connect()
        message = await self.db.llm_chat.find_unique(where={"id": id})
        await self.db.disconnect()
        return message
