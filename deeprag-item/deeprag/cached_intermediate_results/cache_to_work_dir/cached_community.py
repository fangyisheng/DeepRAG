from .. import *


async def cache_community(community_label, community_node, community_report):
    id = [f"{str(uuid.uuid4())}" for _ in community_report]
    data = {
        "id": id,
        "community_label": community_label,
        "community_node": community_node,
        "community_report": community_report
    }
    df = pd.DataFrame(data)
    
    storaged_file_name = f"community_{str(uuid.uuid4())}"

    csv_path = Path.cwd() / "csv_output" / f"{storaged_file_name}.csv"
    df.to_csv(csv_path, index = False)
    
    parquet_path = Path(__file__).parent / "parquet_output" / f"{storaged_file_name}.parquet"
    # parquet_path = 
    df.to_parquet(parquet_path,engine="pyarrow")

    return df
    #返回一个DataFrame对象