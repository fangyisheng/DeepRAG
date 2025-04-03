from deeprag.db.dao.llm_chat.llm_chat_dao import LLMChatDAO
from deeprag.db.data_model import RoleMessage


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
        cost_tokens: str,
    ):
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
        return stored_message.model_dump()

    async def construct_context(self, session_id: str) -> list[RoleMessage]:
        messages = await self.dao.get_message_by_session_id(session_id)
        context = [
            {"role": "user", "content": item}
            for message in messages
            for item in (message.user_prompt, message.user_context)
        ]
        return context
