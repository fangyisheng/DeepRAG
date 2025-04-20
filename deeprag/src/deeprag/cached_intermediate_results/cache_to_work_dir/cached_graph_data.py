from .. import *


async def cache_entity_relation(entity_relation_by_chunk, graph_data):
    data = {
        "human_readable_id": list(range(0, len(entity_relation_by_chunk))),
        "text_chunk_id": [
            f"text_chunk_{str(uuid.uuid4())}"
            for _ in range(0, len(entity_relation_by_chunk))
        ],
        "graph_data": graph_data,
        "graph_data_id": [
            f"graph_data_{str(uuid.uuid4())}"
            for _ in range(0, len(entity_relation_by_chunk))
        ],
    }

    df = pd.DataFrame(data)

    # df = pd.concat([df_from_data, text_chunk_data_frame], axis=1)

    storaged_file_name = f"graph_data_{str(uuid.uuid4())}"

    csv_path = Path.cwd() / "csv_output" / f"{storaged_file_name}.csv"
    df.to_csv(csv_path, index=False)

    parquet_path = (
        Path(__file__).parent / "parquet_output" / f"{storaged_file_name}.parquet"
    )
    # parquet_path =
    df.to_parquet(parquet_path, engine="pyarrow")

    return df
