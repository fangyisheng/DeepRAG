from prisma import Prisma
from prisma.models import index_workflow
from dotenv import load_dotenv

load_dotenv()


class IndexWorkFlowDAO:
    def __init__(self):
        self.db = Prisma()

    async def create_workflow(
        self,
        id: str,
        status: str,
        action: str,
        workflow_start_time: str,
        workflow_end_time: str | None = None,
        workflow_duration_time: str | None = None,
        llm_cost_tokens: int | None = None,
        embedding_cost_tokens: int | None = None,
    ) -> index_workflow:
        await self.db.connect()
        stored_workflow = await self.db.index_workflow.create(
            data={
                "id": id,
                "status": status,
                "action": action,
                "workflow_start_time": workflow_start_time,
                "workflow_end_time": workflow_end_time,
                "workflow_duration_time": workflow_duration_time,
                "llm_cost_tokens": llm_cost_tokens,
                "embedding_cost_tokens": embedding_cost_tokens,
            }
        )
        await self.db.disconnect()
        return stored_workflow

    async def get_workflow_by_id(self, id: str) -> index_workflow:
        await self.db.connect()
        found_workflow = await self.db.workflow.find_unique(where={"id": id})
        await self.db.disconnect()
        return found_workflow

    async def get_workflow_by_message_id(self, message_id: str) -> index_workflow:
        await self.db.connect()
        found_workflow = await self.db.workflow.find_unique(
            where={"message_id": message_id}
        )
        await self.db.disconnect()
        return found_workflow

    async def update_workflow(
        self,
        id: str,
        status: str | None = None,
        action: str | None = None,
        workflow_start_time: str | None = None,
        workflow_end_time: str | None = None,
        workflow_duration_time: str | None = None,
        llm_cost_tokens: int | None = None,
        embedding_cost_tokens: int | None = None,
    ) -> index_workflow:
        await self.db.connect()
        updated_workflow = await self.db.workflow.update(
            where={"id": id},
            data={
                "status": status,
                "action": action,
                "workflow_start_time": workflow_start_time,
                "workflow_end_time": workflow_end_time,
                "workflow_duration_time": workflow_duration_time,
                "llm_cost_tokens": llm_cost_tokens,
                "embedding_cost_tokens": embedding_cost_tokens,
            },
        )
        return updated_workflow


# # 编写测试代码

# import asyncio

# workflow_dao = WorkFlowDAO()


# async def test():
#     data = await workflow_dao.get_workflow_by_id("1")
#     print(data)


# print(asyncio.run(test()))
# # 测试成功
