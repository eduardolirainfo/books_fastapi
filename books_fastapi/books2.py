"""Biblioteca de livros2

Returns:
    _type: dict
"""
from fastapi import FastAPI
from tinydb import TinyDB

app = FastAPI(
    title="Books API",
    description=" API para gerenciar uma biblioteca de livros",
    version="1.0.0",
    reload=True,
)

db = TinyDB("db.json", indent=4, sort_keys=True)


@app.get("/api/v2/books")
async def read_all_books():
    """return all books"""
    return db.all()
