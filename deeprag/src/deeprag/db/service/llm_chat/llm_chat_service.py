from deeprag.db.dao.llm_chat.llm_chat_dao import LLMChatDAO
from deeprag.db.data_model import RoleMessage
from prisma.models import llm_chat
from loguru import logger


class LLMChatService:
    def __init__(self):
        self.dao = LLMChatDAO()

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
        stored_message = await self.dao.create_message(
            id,
            user_id,
            user_prompt,
            user_context,
            llm_answer,
            message_start_time,
            message_end_time,
            message_duration_time,
            session_id,
            llm_token_usage,
            embedding_token_usage,
        )
        return stored_message

    async def construct_context(self, session_id: str) -> list[RoleMessage]:
        messages = await self.dao.get_message_by_session_id(session_id)
        # logger.info(f"messages: {messages}")
        context = [
            RoleMessage(role=role, content=getattr(message, attr))
            for message in messages
            for role, attr in [("user", "user_prompt"), ("assistant", "llm_answer")]
        ]
        return context

    async def get_all_user_prompt_from_context(self, context: list[RoleMessage]) -> str:
        user_prompt_list = [
            message.content for message in context if message.role == "user"
        ]
        all_user_prompt = " ".join(user_prompt_list)
        return all_user_prompt


# # 编写一些测试代码
# llm_chat_service = LLMChatService()
# import asyncio

# a = asyncio.run(
#     llm_chat_service.construct_context("ac956983-c0ca-4463-a4a2-acdf812e791b")
# )
# print(a)
