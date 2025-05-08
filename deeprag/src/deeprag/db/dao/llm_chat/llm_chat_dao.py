from prisma import Prisma
from dotenv import load_dotenv
from prisma.models import llm_chat

load_dotenv()


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
        llm_token_usage: int,
        embedding_token_usage: int,
    ) -> llm_chat:
        if not self.db.is_connected():
            await self.db.connect()
        stored_message = await self.db.llm_chat.create(
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
                "llm_token_usage": llm_token_usage,
                "embedding_token_usage": embedding_token_usage,
            }
        )
        await self.db.disconnect()
        return stored_message

    async def get_message_by_id(self, id: str) -> llm_chat:
        if not self.db.is_connected():
            await self.db.connect()
        found_message = await self.db.llm_chat.find_unique(where={"id": id})
        await self.db.disconnect()
        return found_message

    async def get_message_by_session_id(self, session_id: str) -> list[llm_chat]:
        if not self.db.is_connected():
            await self.db.connect()
        found_message = await self.db.llm_chat.find_many(
            where={"session_id": session_id}
        )
        await self.db.disconnect()
        return found_message


# llm_chat_dao = LLMChatDAO()


# import traceback
# import asyncio


# async def main():
#     try:
#         stored_message = await llm_chat_dao.create_message(
#             id="uudi2",
#             user_id="",
#             user_context=None,
#             user_prompt="user_prompt",
#             llm_answer="llm_answer",
#             message_start_time="message_start_time",
#             message_end_time="message_end_time",
#             message_duration_time="message_duration_time",
#             session_id="session_id",
#             llm_token_usage=0,
#             embedding_token_usage=0,
#         )
#         return stored_message
#     except Exception as e:
#         print(e)
#         print(traceback.format_exc())


# print(asyncio.run(main()))
