from . import *

async def cache_entity_relation(entity_relation_by_chunk, graph_visualization_html, entity_relation_description, text_chunk_data_frame)
    data = {
        "entity_relation_by_chunk": entity_relation_by_chunk,
        "graph_visualization_html": graph_visualization_html,
        "entity_relation_description": entity_relation_description
    }

    df_from_data = pd.DataFrame(data)

    df = pd.concat([df_from_data, text_chunk_data_frame], axis=1)

    storaged_file_name = f"entity_relation_{str(uuid.uuid4())}"

    csv_path = Path.cwd() / "csv_output" / f"{storaged_file_name}.csv"
    df.to_csv(csv_path, index = False)
    
    parquet_path = Path(__file__).parent / "parquet_output" / f"{storaged_file_name}.parquet"
    # parquet_path = 
    df.to_parquet(parquet_path,engine="pyarrow")

    return df