from prisma import Prisma
from prisma.models import community_report
from dotenv import load_dotenv

load_dotenv()


class CommunityReportDAO:
    def __init__(self):
        pass

    async def create_community_report(
        self, id: str, community_report: str, community_id: str
    ) -> community_report:
        async with Prisma() as db:
            stored_community_report = await db.community_report.create(
                data={
                    "id": id,
                    "community_report": community_report,
                    "community_id": community_id,
                }
            )

        return stored_community_report

    async def batch_create_community_report(
        self,
        id_list: list[str],
        community_report_list: list[str],
        community_id_list: list[str],
    ) -> int:
        async with Prisma() as db:
            stored_community_report_count = await db.community_report.create_many(
                data=[
                    {
                        "id": id,
                        "community_report": community_report,
                        "community_id": community_id,
                    }
                    for id, community_report, community_id in zip(
                        id_list, community_report_list, community_id_list
                    )
                ]
            )

        return stored_community_report_count

    async def get_community_report_by_id(self, id: str) -> community_report:
        async with Prisma() as db:
            found_community_report = await db.community_report.find_unique(
                where={"id": id}
            )

        return found_community_report
