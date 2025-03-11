from deeprag.db.service.user.user_service import UserService
from fastapi import APIRouter


user_router = APIRouter(tags=["user"])

user_service = UserService()


@user_service.get("/{id}")
async def get_user_name(id):
    user = await user_service.get_user_name_by_id(id)
    return {
        "msg": "you have gotten the name by id successfully",
        "data": user,
        "code": 200,
    }


@user_router.post("/delete/{id}")
async def delete_user(id):
    user = await user_service.delete_user(id)
    return {"msg": "you have deleted the user successfully", "data": user, "code": 200}
