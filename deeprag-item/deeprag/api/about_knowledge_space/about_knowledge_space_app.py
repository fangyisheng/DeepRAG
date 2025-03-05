from fastapi import APIRouter
import json
from deeprag.db.service.knowledge_space.knowledge_space_service import KnowledgeSpaceService

knowledge_space_router = APIRouter(tags=["knowledge_space"])

class KnowledgeSpace:
    id: str
    human_readable_id: str
    knowledge_space_title: str


knowledge_space_service = KnowledgeSpaceService()

@knowledge_space_router.get("/{id}")
async def get_knowledge_space(knowledge_space_id: str):
    knowledge_space = await knowledge_space_service.get_knowledge_space_by_id(knowledge_space_id)
    return {
        "msg":"get knowledge_space successful",
        "data":knowledge_space,
        "code":200
    }

@knowledge_space_router.post("/")
async def create_knowledge_space(knowledge_space_title):
    knowledge_space = await knowledge_space_service.create_knowledge_space_service(
        knowledge_space_title
    )
    return {
        "msg":"create new knowledge_space successful",
        "data": knowledge_space,
        "code":200
    }

@knowledge_space_router.post("/delete/{id}")
async def delete_knowledge_space(id):
    knowledge_space = await knowledge_space_service.delete_knowledge_space_service(id)
    return {
        "msg":"you have deleted a knowledge_sapce successful",
        "data": knowledge_space,
        "code":200
    }

@knowledge_space_router.post("/update/{id}")
async def update_knowledge_space(id,data):
    knowledge_space = await knowledge_space_service.update_knowledge_space(id,data)
    return {
        "msg":"you have updated the existed knowledge_space in database",
        "data":knowledge_space,
        "code":200
    }




