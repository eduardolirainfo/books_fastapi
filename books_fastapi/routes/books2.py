"""Biblioteca de livros2

Returns:
    _type: dict
"""
from fastapi import APIRouter
from tinydb import where
from ..models.books2 import Books2Request
from ..database import get_database_instance


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
    if book:
        return book
    return {"error": "Book not found"}


@router.get("/byrating/")
async def read_book_by_rating(book_rating: int):
    """Return a book by rating."""
    result = db.search(where("rating") == book_rating)
    if result:
        return result
    return {"error": "Rating not found"}


@router.get("/published/")
async def read_book_by_published_date(book_published_date: int):
    """Return a book by published date."""
    result = db.search(where("published_date") == book_published_date)
    if result:
        return result
    return {"error": "Published date not found"}


@router.post("/create-book")
async def create_book(book_request: Books2Request):
    """Create a new book."""
    new_book = book_request.dict()
    db.insert(new_book)
    return {"success": "book created"}


@router.put("/update-book")
async def update_book(book_request: Books2Request):
    """Update a book."""
    filtro = where("title") == book_request.title
    result = None
    existing_books = db.search(filtro)
    db.upsert(book_request.dict(), filtro)
    if existing_books:
        result = {"success": "book updated"}
    else:
        result = {"success": "book created"}

    if result:
        return result

    return {"error": "Error updating the book"}


@router.delete("/delete-book/{book_title}")
async def delete_book(book_title: str):
    """Delete a book."""
    filtro = where("title") == book_title
    result = None
    existing_books = db.search(filtro)
    db.remove(filtro)
    if existing_books:
        result = {"success": "book deleted"}
    else:
        result = {"error": "book not found"}

    if result:
        return result

    return {"error": "Error deleting the book"}
