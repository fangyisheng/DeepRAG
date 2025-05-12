from prisma import Prisma
from dotenv import load_dotenv
from prisma.models import llm_chat
from deeprag.db.data_model import RoleMessage

load_dotenv()


class LLMChatDAO:
    def __init__(self):
        pass

    async def create_message(
        self,
        id: str,
        user_id: str,
        user_prompt: str,
        user_context: list[RoleMessage],
        llm_answer: str,
        message_start_time: str,
        message_end_time: str,
        message_duration_time: str,
        session_id: str,
        llm_token_usage: int,
        embedding_token_usage: int,
    ) -> llm_chat:
        async with Prisma() as db:
            user_context = str([item.model_dump() for item in user_context])
            stored_message = await db.llm_chat.create(
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

        return stored_message

    async def get_message_by_id(self, id: str) -> llm_chat:
        async with Prisma() as db:
            found_message = await db.llm_chat.find_unique(where={"id": id})

        return found_message

    async def get_message_by_session_id(self, session_id: str) -> list[llm_chat]:
        async with Prisma() as db:
            found_message = await db.llm_chat.find_many(
                where={"session_id": session_id}
            )

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
