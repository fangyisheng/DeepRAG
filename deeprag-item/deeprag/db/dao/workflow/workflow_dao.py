from prisma import Prisma


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
    ):
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
        return stored_workflow.model_dump()

    async def get_workflow_by_id(self, id: str):
        await self.db.connect()
        found_workflow = await self.db.workflow.find_unique(where={"id": id})
        await self.db.disconnect()
        return found_workflow.model_dump()

    async def get_workflow_by_message_id(self, message_id: str):
        await self.db.connect()
        found_workflow = await self.db.workflow.find_unique(
            where={"message_id": message_id}
        )
        await self.db.disconnect()
        return found_workflow.model_dump()
