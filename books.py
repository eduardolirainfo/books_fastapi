"""biblioteca de livros

Returns:
    _type: dict
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """root path for api test"""
    return {"message": "Hello World"}
