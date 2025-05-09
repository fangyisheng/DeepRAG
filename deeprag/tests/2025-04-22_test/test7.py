from deeprag.workflow.text_chunk_process import TextSplitter


async def test_func(a):
    if a > 2:
        text_splitter = TextSplitter()
        return await text_splitter.split_text_by_token(a)
    else:
        
