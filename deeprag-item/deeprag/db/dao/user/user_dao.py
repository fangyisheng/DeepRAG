from prisma import Prisma

class UserDAO:
    def __init__(self):
        self.db = Prisma()

    async def create_user(self, id: str ,  user_name:str):
        await self.db.connect()
        user = await self.db.user.create(
            data = {
                "id": id,
                "user_name": user_name
            }
        )
        await self.db.disconnect()
        return user
    
    async def get_user_name_by_id(self, id: str):
        await self.db.connect()
        user = await self.db.user.find_unique(where={"id":id})
        await self.db.disconnect()
        return user
    
    async def delete_user_by_id(self, id: str):
        await self.db.connect()
        user = await self.db.user.delete(where={"id":id})
        await self.db.disconnect()
        return user