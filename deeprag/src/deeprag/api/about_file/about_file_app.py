from fastapi import APIRouter, HTTPException
from deeprag.db.service.file.file_service import FileService
from deeprag.api.data_model import UploadFileRequestParam

file_router = APIRouter(tags=["files"])

file_service = FileService()


@file_router.get("/{id}")
async def get_file(id):
    found_file = await file_service.get_file_in_knowledge_space_by_knowledge_space_id(
        id
    )
    if not found_file:
        return HTTPException(status_code=404, detail="file not found")
    return {"msg": "get new file successfully", "data": found_file, "code": 200}


@file_router.post("/")
async def upload_file(file: UploadFileRequestParam):
    uploaded_file = await file_service.upload_new_file_to_knowledge_space(
        file.id, file.knowledge_space_id, file.doc_title, file.doc_text
    )
    if not uploaded_file:
        return HTTPException(status_code=404, detail="file upload failed")
    return {
        "msg": "you have uploaded new file in a knowledge_space",
        "data": uploaded_file,
        "code": 200,
    }


@file_router.post("/delete/{id}")
async def delete_file(id: str):
    deleted_file = await file_service.delete_file_in_knowledge_space(id)
    if not deleted_file:
        return HTTPException(
            status_code=404, detail="file delete failed or file has been deleted"
        )
    return {
        "msg": "you have deleted a file in a knowledge_space",
        "data": deleted_file,
        "code": 200,
    }


@file_router.post("/update/{id}")
async def update_file(id: str, data: dict):
    updated_file = await file_service.update_existed_file_in_knowledge_space(id, data)
    return {
        "msg": "you have updated a old file in a knowledge",
        "data": updated_file,
        "code": 200,
    }
