from prisma import Prisma
from dotenv import load_dotenv
from prisma.models import sub_graph_data
from loguru import logger

load_dotenv()


class SubGraphDataDAO:
    def __init__(self):
        pass

    async def create_sub_graph_data(
        self,
        id: str,
        text_chunk_id: str,
        graph_data: str,
        merged_graph_data_id: str,
    ) -> sub_graph_data:
        async with Prisma() as db:
            stored_sub_graph_data = await db.sub_graph_data.create(
                data={
                    "id": id,
                    "text_chunk_id": text_chunk_id,
                    "graph_data": graph_data,
                    "merged_graph_data_id": merged_graph_data_id,
                }
            )

        return stored_sub_graph_data

    async def batch_create_sub_graph_data(
        self,
        id_list: list[str],
        text_chunk_id_list: list[str],
        sub_graph_data_list: list[str],
        merged_graph_data_id: str,
    ) -> int:
        async with Prisma() as db:
            data = [
                {
                    "id": id,
                    "text_chunk_id": text_chunk_id,
                    "graph_data": graph_data,
                    "merged_graph_data_id": merged_graph_data_id,
                }
                for (id, text_chunk_id, graph_data) in zip(
                    id_list, text_chunk_id_list, sub_graph_data_list
                )
            ]
            # logger.info(data)
            stored_sub_graph_data_count = await db.sub_graph_data.create_many(data=data)

        return stored_sub_graph_data_count

    async def get_sub_graph_data_by_id(self, id: str) -> sub_graph_data:
        async with Prisma() as db:
            found_sub_graph_data = await db.sub_graph_data.find_unique(where={"id": id})

        return found_sub_graph_data


# import asyncio

# sub_graph_data_dao = SubGraphDataDAO()
# data = asyncio.run(
#     sub_graph_data_dao.batch_create_sub_graph_data(
#         ["3", "4"],
#         [
#             "b34097cb-a760-46d8-963c-aba4057ac1b5",
#             "4c68ad66-445f-4184-bec5-21deb0f31215",
#         ],
#         ["1", "2"],
#         "e9e7e730-acd6-4ba6-add6-431f795df382",
#     )
# )
# print(data)
