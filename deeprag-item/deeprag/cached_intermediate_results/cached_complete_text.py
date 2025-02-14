from . import *

# 创建示例 DataFrame
async def cache_complete_text(complete_text, file_path):
    data = {
        "id": f"doc_{str(uuid.uuid4())}",
        "text": complete_text,
        "title": Path(file_path).name  
    }
    df = pd.DataFrame(data)
    
    storaged_file_name = f"text_{str(uuid.uuid4())}"

    csv_path = Path.cwd() / "csv_output" / f"{storaged_file_name}.csv"
    df.to_csv(csv_path, index = False)
    
    parquet_path = Path(__file__).parent / "parquet_output" / f"{storaged_file_name}.parquet"
    # parquet_path = 
    df.to_parquet(parquet_path,engine="pyarrow")

    return df
    #返回一个DataFrame对象



