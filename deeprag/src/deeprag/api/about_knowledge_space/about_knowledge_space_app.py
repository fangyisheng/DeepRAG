from fastapi import APIRouter, HTTPException
import json
from deeprag.db.service.knowledge_space.knowledge_space_service import (
    KnowledgeSpaceService,
)
from fastapi.responses import JSONResponse

knowledge_space_router = APIRouter(tags=["knowledge_space"])


# class KnowledgeSpace:
#     id: str
#     human_readable_id: str
#     knowledge_space_title: str


knowledge_space_service = KnowledgeSpaceService()


@knowledge_space_router.get("/{id}")
async def get_knowledge_space(knowledge_space_id: str):
    found_knowledge_space = await knowledge_space_service.get_knowledge_space_by_id(
        knowledge_space_id
    )
    if not found_knowledge_space:
        raise HTTPException(status_code=404, detail="knowledge_space not found")
    result = {
        "msg": "get knowledge_space successful",
        "data": found_knowledge_space.model_dump(),
        "code": 200,
    }

    return JSONResponse(content=result)


@knowledge_space_router.post("/")
async def create_knowledge_space(user_id: str, knowledge_space_name: str):
    created_knowledge_space = await knowledge_space_service.create_knowledge_space(
        user_id=user_id, knowledge_space_name=knowledge_space_name
    )
    if not created_knowledge_space:
        raise HTTPException(status_code=404, detail="knowledge_space create failed")
    result = {
        "msg": "create new knowledge_space successful",
        "data": created_knowledge_space.model_dump(),
        "code": 200,
    }
    return JSONResponse(content=result)


@knowledge_space_router.post("/delete/{id}")
async def delete_knowledge_space(id: str):
    deleted_knowledge_space = await knowledge_space_service.delete_knowledge_space(id)
    if not deleted_knowledge_space:
        raise HTTPException(
            status_code=404,
            detail="knowledge_space delete failed or knowledge_space has been deleted",
        )
    result = {
        "msg": "you have deleted a knowledge_sapce successful",
        "data": deleted_knowledge_space.model_dump(),
        "code": 200,
    }
    return JSONResponse(content=result)


@knowledge_space_router.post("/update/{id}")
async def update_knowledge_space(id: str, data: dict):
    updated_knowledge_space = await knowledge_space_service.update_knowledge_space(
        id, data
    )
    if not updated_knowledge_space:
        raise HTTPException(
            status_code=404,
            detail="knowledge_space update failed",
        )
    result = {
        "msg": "you have updated the existed knowledge_space in database",
        "data": updated_knowledge_space.model_dump(),
        "code": 200,
    }
    return JSONResponse(content=result)
