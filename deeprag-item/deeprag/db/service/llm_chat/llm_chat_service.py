from deeprag.db.dao.llm_chat.llm_chat_dao import LLMChatDAO


class LLMChatService:
    def __init__(self):
        self.dao = LLMChatDAO()


    async def chat_completions(user_prompt,model,temperature,stream):