from deeprag.rag_core_utils.llm_api.llm_api_client import llm_chat, llm_chat_not_stream
from deeprag.prompts.dynamic_prompts.rag_answer_prompt import rag_answer_prompt_content
from deeprag.workflow.data_model import (
    FinalRAGAnswerResponse,
    FinalRAGAnswerStreamResponse,
)

from deeprag.db.data_model import RoleMessage
from typing import AsyncGenerator


async def final_rag_answer_process_stream(
    user_prompt: str,
    knowledge_space_name: str,
    searched_file_name: str,
    searched_file_context: str,
    session_id: str,
    message_id: str,
    context: list[RoleMessage] | None = None,
) -> AsyncGenerator[FinalRAGAnswerStreamResponse, None]:
    system_prompt = rag_answer_prompt_content(
        knowledge_space_name, searched_file_name, searched_file_context
    )

    response = llm_chat(system_prompt, context, user_prompt)
    async for answer in response:
        message = {
            "answer": answer,
            "rag_pattern": "common",
            "session_id": session_id,
            "message_id": message_id,
        }
        yield f"data: {message}\n\n"


async def final_rag_answer_process_not_stream(
    user_prompt: str,
    knowledge_space_name: str,
    searched_file_name: str,
    searched_file_context: str,
    session_id: str,
    message_id: str,
    context: list | None = None,
) -> FinalRAGAnswerResponse:
    system_prompt = rag_answer_prompt_content(
        knowledge_space_name, searched_file_name, searched_file_context
    )

    answer = llm_chat_not_stream(system_prompt, context, user_prompt)

    message = {
        "answer": answer,
        "rag_pattern": "common",
        "session_id": session_id,
        "message_id": message_id,
    }
    return message
