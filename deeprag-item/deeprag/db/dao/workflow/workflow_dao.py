from prisma import Prisma
from prisma.models import workflow
from dotenv import load_dotenv

load_dotenv()


class WorkFlowDAO:
    def __init__(self):
        self.db = Prisma()

    async def create_workflow(
        self,
        id: str,
        status: str,
        action: str,
        workflow_start_time: str,
        workflow_end_time: str,
        workflow_duration_time: str,
    ) -> workflow:
        await self.db.connect()
        stored_workflow = await self.db.workflow.create(
            data={
                "id": id,
                "status": status,
                "action": action,
                "workflow_start_time": workflow_start_time,
                "workflow_end_time": workflow_end_time,
                "workflow_duration_time": workflow_duration_time,
            }
        )
        await self.db.disconnect()
        return stored_workflow

    async def get_workflow_by_id(self, id: str) -> workflow:
        await self.db.connect()
        found_workflow = await self.db.workflow.find_unique(where={"id": id})
        await self.db.disconnect()
        return found_workflow

    async def get_workflow_by_message_id(self, message_id: str) -> workflow:
        await self.db.connect()
        found_workflow = await self.db.workflow.find_unique(
            where={"message_id": message_id}
        )
        await self.db.disconnect()
        return found_workflow


# # 编写测试代码

# import asyncio

# workflow_dao = WorkFlowDAO()


# async def test():
#     data = await workflow_dao.get_workflow_by_id("1")
#     print(data)


# print(asyncio.run(test()))
# # 测试成功
