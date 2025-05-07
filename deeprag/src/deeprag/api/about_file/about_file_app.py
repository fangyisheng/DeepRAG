from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from fastapi.responses import JSONResponse
from deeprag.db.service.file.file_service import FileService
from deeprag.api.data_model import UploadFileRequestParam
from deeprag.core import DeepRAG
from io import BytesIO

file_router = APIRouter(tags=["files"])

file_service = FileService()

deeprag = DeepRAG()


@file_router.get("/{id}")
async def get_file_by_file_id(id: str):
    found_file = await file_service.get_file_in_knowledge_space_by_doc_id(id)
    if not found_file:
        return HTTPException(status_code=404, detail="file not found")
    result = {
        "msg": "get new file successfully",
        "data": found_file.model_dump(),
        "code": 200,
    }
    return JSONResponse(content=result)


@file_router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    knowledge_space_id: str = Form(...),
    minio_bucket_name: str = Form(...),
    minio_object_name: str = Form(...),
):
    file_content = await file.read()
    file_stream = BytesIO(file_content)
    # uploaded_file = await file_service.upload_new_file_to_knowledge_space(
    #     knowledge_space_id=knowledge_space_id,
    #     doc_title=file.filename,
    #     doc_text=None,
    #     minio_bucket_name=MINIO_BUCKET_NAME,
    #     minio_object_name=file.filename,
    #     file_path=None,
    #     metadata=None,
    # )
    uploaded_file = await deeprag.create_file_and_upload_to_minio(
        knowledge_space_id=knowledge_space_id,
        bucket_name=minio_bucket_name,
        object_name=minio_object_name,
        io_data=file_stream,
    )
    if not uploaded_file:
        return HTTPException(status_code=404, detail="file upload failed")
    result = {
        "msg": "you have uploaded new file in a knowledge_space",
        "data": uploaded_file.model_dump(),
        "code": 200,
    }

    return JSONResponse(content=result)


@file_router.post("/delete/{id}")
async def delete_file(id: str):
    deleted_file = await file_service.delete_file_in_knowledge_space(id)
    if not deleted_file:
        return HTTPException(
            status_code=404, detail="file delete failed or file has been deleted"
        )
    result = {
        "msg": "you have deleted a file in a knowledge_space",
        "data": deleted_file.model_dump(),
        "code": 200,
    }

    return JSONResponse(content=result)


@file_router.post("/update/{id}")
async def update_file(id: str, data: dict):
    updated_file = await file_service.update_existed_file_in_knowledge_space(id, data)
    result = {
        "msg": "you have updated a old file in a knowledge",
        "data": updated_file.model_dump(),
        "code": 200,
    }
    return JSONResponse(content=result)
