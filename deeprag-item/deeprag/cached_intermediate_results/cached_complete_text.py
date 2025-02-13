import pandas as pd
from tabulate import tabulate
import uuid
# 创建示例 DataFrame
async def cache_complete_text(complete_text):
    data = {
        "id":f"doc_{str(uuid.uuid4())}",
        "text": complete_text,
        
    }