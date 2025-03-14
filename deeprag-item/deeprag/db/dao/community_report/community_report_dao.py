from prisma import Prisma


class CommunityReportDAO:
    def __init__(self):
        self.db = Prisma()

    async def create_community_report(
        self, id: str, community_report: str, community_id: str
    ):
        await self.db.connect()
        community_report = await self.db.community_report.create(
            data={
                "id": id,
                "community_report": community_report,
                "community_id": community_id,
            }
        )
        await self.db.disconnect()
        return community_report

    async def get_community_report_by_id(self, id: str):
        await self.db.connect()
        community_report = await self.db.community_report.find_unique(where={"id": id})
        await self.db.disconnect()
        return community_report
