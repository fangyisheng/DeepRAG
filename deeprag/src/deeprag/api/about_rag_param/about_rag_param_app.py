from fastapi import APIRouter, HTTPException
from deeprag.db.service.rag_param.rag_param_service import RagParamService
from fastapi.responses import JSONResponse

rag_param_service = RagParamService()

rag_param_router = APIRouter(tags=["rag_param"])


@rag_param_router.get("/{message_id}")
async def get_merged_graph_data(message_id: str):
    found_rag_param = await rag_param_service.get_rag_param_by_message_id(message_id)
    if not found_rag_param:
        raise HTTPException(status_code=404, detail="rag_param not found")
    result = {
        "msg": "get merged_graph_data successfully",
        "data": found_rag_param.model_dump(),
        "code": 200,
    }
    return JSONResponse(content=result)
