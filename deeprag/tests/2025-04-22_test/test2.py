import asyncio
from tqdm import tqdm

import asyncio
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
)


async def do_work(x):
    await asyncio.sleep(x)
    return x


async def main():
    tasks = [asyncio.create_task(do_work(i)) for i in [3, 1, 2, 5, 4]]
    total = len(tasks)

    progress = Progress(
        SpinnerColumn(),  # 小动画
        BarColumn(bar_width=None),  # 彩色进度条
        "[progress.percentage]{task.percentage:>3.0f}%",  # 百分比
        TimeElapsedColumn(),  # 已用时间
        TextColumn("[cyan]Processing..."),  # 文本
    )

    with progress:
        task_id = progress.add_task("Working", total=total)

        for future in asyncio.as_completed(tasks):
            result = await future
            progress.advance(task_id)
            # 这里可以处理 result，比如打印


asyncio.run(main())
