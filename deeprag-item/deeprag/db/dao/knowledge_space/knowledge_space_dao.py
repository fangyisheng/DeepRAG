from prisma import Prisma

class KnowledgeSpaceDAO:
    def __init__(self):
        self.db = Prisma()

    async def create_knowledge_space(self, id: str , knowledge_space_id: str,knowledge_space_title: str):
        await self.db.connect()
        knowledge_space = await self.db.knowledge_space.create(
            data = {
                "id": id,
                "knowledge_space_id": knowledge_space_id,
                "knowledge_space_title": knowledge_space_title
            }
        )
        await self.db.disconnect()
        return knowledge_space
    
    async def delete_knowledge_space(self, knowledge_space_id: str):
        await self.db.connect()
        knowledge_space = await self.db.knowledge_space.delete(where={"knowledge_space_id":knowledge_space_id})
        await self.db.connect()
        return knowledge_space
    
    async def query_by_knowledge_space_id(self, knowledge_space_id: str):
        await self.db.connect()
        knowledge_space = await self.db.knowledge_space.find_unique(where={"knowledge_space_id":knowledge_space_id})
        await self.db.connect()
        return knowledge_space
    
    async def update_knowledge_space(self,  knowledge_space_id: str, data: dict):
        await self.db.connect()
        knowledge_space = await self.db.knowledge_space.update(
            where = {"knowledge_space_id":knowledge_space_id},
            data = data
        )
        await self.db.disconnect()
        return knowledge_space
    