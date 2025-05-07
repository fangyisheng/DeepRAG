from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from deeprag.core import DeepRAG
from deeprag.api.data_model import BatchIndexRequestParam

batch_index_router = APIRouter(tags=["batch_index"])

deeprag = DeepRAG()


@batch_index_router.post("/")
async def index(request: BatchIndexRequestParam):
    index_result = await deeprag.batch_index(
        collection_name=request.collection_name,
        knowledge_scope=request.knowledge_scope,
        meta_data=request.meta_data,
        deep_index_pattern=request.deep_index_pattern,
    )
    if not index_result:
        raise HTTPException(status_code=500, detail="Index failed")
    result = {"msg": "Index success", "data": index_result.model_dump(), "code": 200}
    return JSONResponse(content=result)
