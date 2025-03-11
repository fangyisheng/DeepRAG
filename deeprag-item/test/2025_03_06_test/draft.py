def greet(name: str | None = None) -> str:
    if name is None:
        return "Hello, Guest!"
    else:
        return f"Hello, {name}!"


print(greet())
