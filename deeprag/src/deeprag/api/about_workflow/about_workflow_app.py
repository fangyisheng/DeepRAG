from fastapi import APIRouter, HTTPException
from deeprag.db.service.index_workflow.index_workflow_service import (
    IndexWorkFlowService,
)
from fastapi.responses import JSONResponse

workflow_router = APIRouter(tags=["workflow"])

workflow_service = IndexWorkFlowService()


@workflow_router.get("/{id}")
async def get_workflow(id: str):
    found_workflow = await workflow_service.get_workflow_by_id(id)
    if not found_workflow:
        raise HTTPException(status_code=404, detail="workflow not found")
    result = {
        "msg": "work is flowing",
        "data": found_workflow.model_dump(),
        "code": 200,
    }
    return JSONResponse(content=result)
