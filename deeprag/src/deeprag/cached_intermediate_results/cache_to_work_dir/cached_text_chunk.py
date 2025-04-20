from .. import *


async def cache_text_chunk(chunks_list, tokens_by_chunk, doc_id, doc_title):
    chunk_id = [f"chunk_{str(uuid.uuid4())}" for _ in chunks_list]
    id = [f"{str(uuid.uuid4())}" for _ in chunks_list]

    data = {
        "id": id,
        "chunk": chunks_list,
        "chunk_id": chunk_id,
        "chunk_token": tokens_by_chunk,
        "doc_id": doc_id,
        "doc_title": doc_title,
    }

    df = pd.DataFrame(data)

    storaged_file_name = f"text_chunk_{str(uuid.uuid4())}"

    csv_path = Path.cwd() / "csv_output" / f"{storaged_file_name}.csv"
    df.to_csv(csv_path, index=False)

    parquet_path = (
        Path(__file__).parent / "parquet_output" / f"{storaged_file_name}.parquet"
    )
    # parquet_path =
    df.to_parquet(parquet_path, engine="pyarrow")

    return df
