from fastapi import APIRouter, HTTPException
from deeprag.db.service.text_chunk.text_chunk_service import TextChunkService
from fastapi.responses import JSONResponse

text_chunk_service = TextChunkService()


text_chunk_router = APIRouter(tags=["text_chunk"])


@text_chunk_router.get("/{id}")
async def get_text_chunk(id: str):
    found_text_chunk = await text_chunk_service.get_text_chunk_by_id(id)
    if not found_text_chunk:
        raise HTTPException(status_code=404, detail="text_chunk not found")
    result = {
        "msg": "get text_chunk successfully",
        "data": found_text_chunk.model_dump(),
        "code": 200,
    }
    return JSONResponse(content=result)
