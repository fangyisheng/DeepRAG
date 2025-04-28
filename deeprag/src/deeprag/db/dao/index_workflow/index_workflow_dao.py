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
        found_workflow = await self.db.index_workflow.find_unique(where={"id": id})
        await self.db.disconnect()
        return found_workflow

    async def get_workflow_by_message_id(self, message_id: str) -> index_workflow:
        await self.db.connect()
        found_workflow = await self.db.index_workflow.find_unique(
            where={"message_id": message_id}
        )
        await self.db.disconnect()
        return found_workflow

    async def update_workflow(self, id: str, data: dict) -> index_workflow:
        await self.db.connect()
        # data = {}
        # if status is not None:
        #     data["status"] = status
        # if action is not None:
        #     data["action"] = action
        # if workflow_start_time is not None:
        #     data["workflow_start_time"] = workflow_start_time
        # if workflow_end_time is not None:
        #     data["workflow_end_time"] = workflow_end_time
        # if workflow_duration_time is not None:
        #     data["workflow_duration_time"] = workflow_duration_time
        # if llm_cost_tokens is not None:
        #     data["llm_cost_tokens"] = llm_cost_tokens
        # if embedding_cost_tokens is not None:
        #     data["embedding_cost_tokens"] = embedding_cost_tokens
        updated_workflow = await self.db.index_workflow.update(
            where={"id": id},
            data=data,
        )
        await self.db.disconnect()
        return updated_workflow


# # 编写测试代码

# import asyncio

# workflow_dao = WorkFlowDAO()


# async def test():
#     data = await workflow_dao.get_workflow_by_id("1")
#     print(data)


# print(asyncio.run(test()))
# # 测试成功


# # 做一下update的功能方法测试
# import asyncio


# async def test():
#     index_workflow_dao = IndexWorkFlowDAO()
#     data = await index_workflow_dao.update_workflow(
#         id="5a753960-4547-4afe-915d-7c0d6cfc3bdd", action=None
#     )

#     print(data)


# asyncio.run(test())
