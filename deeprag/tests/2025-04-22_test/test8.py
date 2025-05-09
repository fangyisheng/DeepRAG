from deeprag.workflow.text_chunk_process import TextSplitter

from deeprag.workflow.text_extract_and_clean import process_text
import asyncio

splitter = TextSplitter()


async def test(bucket_name, object_name):
    complete_text = await process_text(bucket_name, object_name)
    result = await splitter.split_text_by_row_in_csv(complete_text)
    return result.root


asyncio.run(test("mybucket", "test.csv"))
