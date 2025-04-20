from deeprag.db.dao.workflow.workflow_dao import WorkFlowDAO


class WorkFlowService:
    def __init__(self):
        self.dao = WorkFlowDAO()

    async def get_workflow_by_id(self, id: str):
        workflow = await self.dao.get_workflow_by_id(id)
        return workflow.__dict__  # 这边的返回需要定制一下 毕竟是Service层

    async def get_workflow_by_message_id(self, message_id: str):
        workflow = await self.dao.get_workflow_by_message_id(message_id)
        return workflow.__dict__  # 这边的返回需要定制一下 毕竟是Service层
