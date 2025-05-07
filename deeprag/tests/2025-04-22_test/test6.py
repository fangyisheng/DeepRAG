from fastapi import HTTPException


def test_func():
    print("test")
    raise HTTPException(status_code=400, detail="test")


print(test_func())
