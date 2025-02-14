import pandas as pd
from tabulate import tabulate
import uuid
from pathlib import Path


# 创建示例 DataFrame
async def cache_complete_text(complete_text,title):
    data = {
        "id":f"doc_{str(uuid.uuid4())}",
        "text": complete_text,
        "title": title
    }
    df = pd.DataFrame(data)
    
    df.to_csv()
    
    # parquet_path = 
    df.to_parquet()

    return df
    #返回一个DataFrame对象


# from pathlib import Path

# def test():
#     print(Path.cwd())