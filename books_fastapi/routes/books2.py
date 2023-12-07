"""Biblioteca de livros2

Returns:
    _type: dict
"""
from fastapi import APIRouter
from ..models.books2 import Books2Request
from ..database import get_database_instance

router = APIRouter()

db = get_database_instance("db2")


@router.get("/")
async def read_all_books():
    """Return all books."""
    return db.all()


@router.post("/create-book")
async def create_book(book_request: Books2Request):
    """Create a new book."""

    new_book = book_request.dict()
    db.insert(new_book)
    return new_book
