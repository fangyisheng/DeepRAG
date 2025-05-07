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
import json


async def final_rag_answer_process_stream(
    user_prompt: str,
    knowledge_scope_real_name: KnowledgeScopeRealName,
    recalled_text_fragments_list: list[str],
    session_id: str,
    embedding_token_usage: int,
    deep_query_pattern: bool = False,
    context: list[RoleMessage] | None = None,
) -> AsyncGenerator[FinalRAGAnswerStreamResponse, None]:
    recalled_text_fragments = "\n".join(recalled_text_fragments_list)
    system_prompt = rag_answer_prompt_content(
        knowledge_scope_real_name, recalled_text_fragments
    )
    if not context:
        response = await llm_chat(system_prompt=system_prompt, user_prompt=user_prompt)
    else:
        context = str([item.model_dump() for item in context])
        response = await llm_chat(
            system_prompt=system_prompt,
            context_histroy=context,
            user_prompt=user_prompt,
        )
    if not session_id:
        session_id = str(uuid.uuid4())

    message_id = str(uuid.uuid4())
    async for answer in response.assistant_response_generator:
        message = {
            "answer": answer,
            "rag_pattern": "deep_query_pattern"
            if deep_query_pattern
            else "common_query_pattern",
            "rag_groundings": recalled_text_fragments,
            "session_id": session_id,
            "message_id": message_id,
        }
        yield f"data: {json.dumps(message, ensure_ascii=False)}\n\n"
    last_message = {
        "answer": "",
        "rag_pattern": "deep_query_pattern"
        if deep_query_pattern
        else "common_query_pattern",
        "rag_groundings": recalled_text_fragments,
        "session_id": session_id,
        "message_id": message_id,
        "embedding_token_usage": embedding_token_usage,
        "llm_token_usage": response.cost_tokens.result(),
    }
    yield f"data: {json.dumps(last_message, ensure_ascii=False)}\n\n"


async def final_rag_answer_process_not_stream(
    user_prompt: str,
    knowledge_scope_real_name: KnowledgeScopeRealName,
    recalled_text_fragments_list: list[str],
    session_id: str,
    embedding_token_usage: int,
    deep_query_pattern: bool = False,
    context: list[RoleMessage] | None = None,
) -> FinalRAGAnswerResponse:
    recalled_text_fragments = "\n".join(recalled_text_fragments_list)
    system_prompt = rag_answer_prompt_content(
        knowledge_scope_real_name, recalled_text_fragments
    )

    if not context:
        answer = await llm_chat_not_stream(
            system_prompt=system_prompt, user_prompt=user_prompt
        )
    else:
        context = str([item.model_dump() for item in context])
        answer = await llm_chat_not_stream(
            system_prompt=system_prompt,
            context_histroy=context,
            user_prompt=user_prompt,
        )
    if not session_id:
        session_id = str(uuid.uuid4())
    message_id = str(uuid.uuid4())

    message = {
        "answer": answer.assistant_response,
        "rag_pattern": "deep_query_pattern"
        if deep_query_pattern
        else "common_query_pattern",
        "rag_groundings": recalled_text_fragments,
        "session_id": session_id,
        "message_id": message_id,
        "embedding_token_usage": embedding_token_usage,
        "llm_token_usage": answer.cost_tokens,
    }
    return message
