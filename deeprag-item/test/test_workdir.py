from deeprag.cached_intermediate_results.cache_to_work_dir.cached_complete_text import test

test()


import pandas as pd

# 创建一个简单的数据字典
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
}

print(data)

# 使用数据字典创建 DataFrame
df = pd.DataFrame(data)

print(df)

