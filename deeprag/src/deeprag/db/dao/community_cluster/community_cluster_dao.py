from prisma import Prisma
from prisma.models import community_cluster
from dotenv import load_dotenv

load_dotenv()


class CommunityClusterDAO:
    def __init__(self):
        pass

    async def create_community_cluster(
        self, id: str, community: str, community_title: str
    ) -> community_cluster:
        async with Prisma() as db:
            stored_community_cluster = await db.community_cluster.create(
                data={
                    "id": id,
                    "community": community,
                    "community_title": community_title,
                }
            )

        return stored_community_cluster

    async def get_community_cluster_by_id(self, id: str) -> community_cluster:
        async with Prisma() as db:
            found_community_cluster = await db.community_cluster.find_unique(
                where={"id": id}
            )

        return found_community_cluster

    async def batch_create_community_cluster(
        self, community_cluster_list: list[dict[str, str]]
    ) -> int:
        async with Prisma() as db:
            stored_community_cluster_list = await db.community_cluster.create_many(
                data=community_cluster_list
            )

        return stored_community_cluster_list
