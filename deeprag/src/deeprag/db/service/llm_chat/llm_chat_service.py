from deeprag.db.dao.llm_chat.llm_chat_dao import LLMChatDAO
from deeprag.db.data_model import RoleMessage
from prisma.models import llm_chat


class LLMChatService:
    def __init__(self):
        self.dao = LLMChatDAO()

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
        cost_tokens: str | None = None,
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
            cost_tokens,
        )
        return stored_message

    async def construct_context(self, session_id: str) -> list[RoleMessage]:
        messages = await self.dao.get_message_by_session_id(session_id)
        context = [
            RoleMessage(role=role, content=getattr(message, attr))
            for message in messages
            for role, attr in [("user", "user_prompt"), ("assistant", "llm_answer")]
        ]
        return context
