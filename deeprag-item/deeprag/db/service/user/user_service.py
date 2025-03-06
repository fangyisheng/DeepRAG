from deeprag.db.dao.user.user_dao import UserDAO

class UserService:
    def __init__(self):
        self.dao = UserDAO()
    
    async def get_user_name_by_id(self,id: str):
        user = await self.dao.get_user_name_by_id(id)
        return user.__dict__
    
    async def delete_user(self, id:str):
        user = await self.dao.delete_user_by_id(id)
        return user.__dict__
