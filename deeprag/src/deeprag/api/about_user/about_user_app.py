from deeprag.db.service.user.user_service import UserService
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

user_router = APIRouter(tags=["user"])

user_service = UserService()


@user_router.get("/{id}")
async def get_user_name(id: str):
    found_user = await user_service.get_user_name_by_id(id)
    if not found_user:
        raise HTTPException(status_code=404, detail="User not found")
    result = {
        "msg": "you have gotten the name by id successfully",
        "data": found_user.model_dump(),
        "code": 200,
    }

    return JSONResponse(content=result)


@user_router.post("/delete/{id}")
async def delete_user(id: str):
    deleted_user = await user_service.delete_user(id)
    if not deleted_user:
        raise HTTPException(
            status_code=404, detail="delete user failed or user has been deleted"
        )
    result = {
        "msg": "you have deleted the user successfully",
        "data": deleted_user.model_dump(),
        "code": 200,
    }
    return JSONResponse(content=result)


@user_router.post("/")
async def create_user(user_name: str):
    created_user = await user_service.create_user(user_name)
    if not created_user:
        raise HTTPException(status_code=404, detail="create user failed")
    result = {
        "msg": "you have created the user successfully",
        "data": created_user.model_dump(),
        "code": 200,
    }

    return JSONResponse(content=result)
