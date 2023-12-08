"""Biblioteca de livros2

Returns:
    _type: dict
"""
from fastapi import APIRouter, HTTPException
from ..models.books2 import Books2Request
from ..database import get_database_instance
from tinydb import where

router = APIRouter()

db = get_database_instance("db2")


@router.get("/")
async def read_all_books():
    """Return all books."""
    return db.all()


@router.get("/{book_id}")
async def read_book_by_id(book_id: int):
    """Return a book by id."""
    book = db.get(doc_id=book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get("/byrating/")
async def read_book_by_rating(book_rating: int):
    """Return a book by rating."""
    result = db.search(where("rating") == book_rating)
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    return result


@router.post("/create-book")
async def create_book(book_request: Books2Request):
    """Create a new book."""

    new_book = book_request.dict()
    db.insert(new_book)
    return new_book
