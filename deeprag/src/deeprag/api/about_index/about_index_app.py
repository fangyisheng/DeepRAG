from fastapi import APIRouter, HTTPException
from deeprag.core import DeepRAG
from deeprag.api.data_model import IndexRequestParam, BatchIndexRequestParam

index_router = APIRouter(tags=["index"])

deeprag = DeepRAG()


@index_router.post("/")
async def index(request: IndexRequestParam):
    index_result = await deeprag.index(
        collection_name=request.collection_name,
        knowledge_scope=request.knowledge_scope,
        meta_data=request.meta_data,
        deep_index_pattern=request.deep_index_pattern,
    )
    if not index_result:
        raise HTTPException(status_code=500, detail="Index failed")
    return {"msg": "Index success", "data": index_result.model_dump(), "code": 200}
