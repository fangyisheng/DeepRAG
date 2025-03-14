import tiktoken


def compute_token(text):
    encoding = tiktoken.encoding_for_model("gpt-4o")

    tokens = encoding.encode(text)
    return len(tokens)
