from fastapi import APIRouter
from deeprag.db.service.file.file_service import FileService

file_router = APIRouter(tags=["file"])

file_service = FileService()


@file_router.get("/")
async def get_file(id):
    file = await file_service.get_file_in_knowledge_space_by_doc_id_service(id)
    return {"msg": "get new file successfully", "data": file, "code": 200}


@file_router.post("/{id}")
async def upload_file(id, doc_text, knowledge_space_id, doc_title):
    file = await file_service.upload_new_file_to_knowledge_space_service(
        id, knowledge_space_id, doc_title, doc_text
    )
    return {
        "msg": "you have uploaded new file in a knowledge_space",
        "data": file,
        "code": 200,
    }


@file_router.post("/delete/{id}")
async def delete_file(id):
    file = await file_service.delete_file_in_knowledge_space_service(id)
    return {
        "msg": "you have deleted a file in a knowledge_space",
        "data": file,
        "code": 200,
    }


@file_router.post("/update/{id}")
async def update_file(id, data):
    file = await file_service.update_existed_file_in_knowledge_space_service(id, data)
    return {
        "msg": "you have updated a old file in a knowledge",
        "data": file,
        "code": 200,
    }
