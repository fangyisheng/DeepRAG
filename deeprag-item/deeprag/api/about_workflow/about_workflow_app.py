from fastapi import APIRouter
from deeprag.db.service.workflow.workflow_service import WorkFlowService

workflow_router = APIRouter(tags = ["workflow"])

workflow_service = WorkFlowService()

@workflow_router.get("/{id}")
async def get_workflow(id):
    workflow = await workflow_service.get_workflow_by_id()
    return {
        "msg":"work is flowing",
        "data":workflow,
        "code":200
    }