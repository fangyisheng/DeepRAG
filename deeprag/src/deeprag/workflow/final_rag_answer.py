from deeprag.rag_core_utils.llm_api.llm_api_client import llm_chat, llm_chat_not_stream
from deeprag.prompts.dynamic_prompts.rag_answer_prompt import rag_answer_prompt_content
from deeprag.workflow.data_model import (
    FinalRAGAnswerResponse,
    FinalRAGAnswerStreamResponse,
    KnowledgeScopeRealName,
)

from deeprag.db.data_model import RoleMessage
from typing import AsyncGenerator
import uuid


async def final_rag_answer_process_stream(
    user_prompt: str,
    knowledge_scope_real_name: KnowledgeScopeRealName,
    recalled_text_fragments_list: list[str],
    session_id: str,
    deep_query_pattern: bool = False,
    context: list[RoleMessage] | None = None,
) -> AsyncGenerator[FinalRAGAnswerStreamResponse, None]:
    recalled_text_fragments = "\n".join(recalled_text_fragments_list)
    system_prompt = rag_answer_prompt_content(
        knowledge_scope_real_name, recalled_text_fragments
    )
    if not context:
        response = llm_chat(system_prompt, user_prompt=user_prompt)
    else:
        response = llm_chat(system_prompt, context, user_prompt)
    if not session_id:
        session_id = str(uuid.uuid4())

    message_id = str(uuid.uuid4())
    async for answer in response:
        message = {
            "answer": answer,
            "rag_pattern": "deep_query_pattern"
            if deep_query_pattern
            else "common_query_pattern",
            "session_id": session_id,
            "message_id": message_id,
        }
        yield f"data: {message}\n\n"


async def final_rag_answer_process_not_stream(
    user_prompt: str,
    knowledge_scope_real_name: KnowledgeScopeRealName,
    recalled_text_fragments_list: list[str],
    session_id: str,
    deep_query_pattern: bool = False,
    context: list[RoleMessage] | None = None,
) -> FinalRAGAnswerResponse:
    recalled_text_fragments = "\n".join(recalled_text_fragments_list)
    system_prompt = rag_answer_prompt_content(
        knowledge_scope_real_name, recalled_text_fragments
    )

    if not context:
        answer = await llm_chat_not_stream(system_prompt, user_prompt=user_prompt)
    else:
        context = 
        answer = await llm_chat_not_stream(system_prompt, context, user_prompt)
    if not session_id:
        session_id = str(uuid.uuid4())
    message_id = str(uuid.uuid4())

    message = {
        "answer": answer.assistant_response,
        "rag_pattern": "deep_query_pattern"
        if deep_query_pattern
        else "common_query_pattern",
        "session_id": session_id,
        "message_id": message_id,
    }
    return message
