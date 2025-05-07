from fastapi import FastAPI, APIRouter
from fastapi.responses import StreamingResponse, JSONResponse
from deeprag.core import DeepRAG
from deeprag.api.data_model import ChatRequestParam


chat_router = APIRouter(tags=["chat"])


deeprag = DeepRAG()


@chat_router.post("/completions")
async def chat_completions(chat: ChatRequestParam):
    if chat.stream:
        generator = deeprag.query_by_stream(
            user_prompt=chat.user_prompt,
            knowledge_scope=chat.knowledge_scope,
            deep_query_pattern=chat.deep_query_pattern,
            session_id=chat.session_id,
            context=chat.context,
            recalled_text_fragments_top_k=chat.recalled_text_fragments_top_k,
        )
        return StreamingResponse(generator, media_type="text/event-stream")
    else:
        result = await deeprag.query_by_non_stream(
            user_prompt=chat.user_prompt,
            knowledge_scope=chat.knowledge_scope,
            deep_query_pattern=chat.deep_query_pattern,
            session_id=chat.session_id,
            context=chat.context,
            recalled_text_fragments_top_k=chat.recalled_text_fragments_top_k,
        )
        return JSONResponse(content=result)
