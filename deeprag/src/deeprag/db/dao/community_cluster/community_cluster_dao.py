from prisma import Prisma
from prisma.models import community_cluster
from dotenv import load_dotenv

load_dotenv()


class CommunityClusterDAO:
    def __init__(self):
        self.db = Prisma()

    async def create_community_cluster(
        self, id: str, community: str, community_title: str
    ) -> community_cluster:
        await self.db.connect()
        stored_community_cluster = await self.db.community_cluster.create(
            data={"id": id, "community": community, "community_title": community_title}
        )
        await self.db.disconnect()
        return stored_community_cluster

    async def get_community_cluster_by_id(self, id: str) -> community_cluster:
        await self.db.connect()
        found_community_cluster = await self.db.community_cluster.find_unique(
            where={"id": id}
        )
        await self.db.disconnect()
        return found_community_cluster

    async def batch_create_community_cluster(
        self, community_cluster_list: list[dict]
    ) -> int:
        await self.db.connect()
        stored_community_cluster_list = await self.db.community_cluster.create_many(
            data=community_cluster_list
        )
        await self.db.disconnect()
        return stored_community_cluster_list
