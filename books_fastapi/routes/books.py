"""Biblioteca de livros

Returns:
    _type: dict
"""
import re
from fastapi import Body, APIRouter
from tinydb import where
from ..database import get_database_instance


router = APIRouter()
db = get_database_instance("db")


@router.get("/")
async def read_all_books():
    """return all books"""
    return db.all()


@router.get("/{book_title}")
async def read_book_title(book_title: str):
    """return book by title"""
    book_title = book_title.strip()
    result = db.search(
        where("title").matches(f".*{re.escape(book_title)}.*", flags=re.IGNORECASE)
    )
    if result:
        return result

    return {"error": "book not found"}


@router.get("/category/")
async def read_category_by_query(book_category: str):
    """return book by category"""
    book_category = book_category.strip()
    result = db.search(
        where("category").matches(
            f".*{re.escape(book_category)}.*", flags=re.IGNORECASE
        )
    )
    if result:
        return result
    return {"error": "Categoria não encontrada"}


@router.get("/byauthor/")
async def read_books_by_author_path(author: str):
    """return book by author"""
    result = db.search(where("author").matches(author, flags=re.IGNORECASE))
    if result:
        return result
    return {"error": "Autor não encontrado"}


@router.get("/bycategory/")
async def read_books_by_category_path(category: str):
    """return book by category"""
    result = db.search(where("category").matches(category, flags=re.IGNORECASE))
    if result:
        return result
    return {"error": "category not found"}


@router.get("/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    """return book by author and category"""
    result = db.search(
        (where("author").matches(book_author, flags=re.IGNORECASE))
        & (where("category").matches(category, flags=re.IGNORECASE))
    )

    if result:
        return result
    return {"error": "author or category not found"}


@router.post("/create_book")
async def create_book(new_book: dict = Body(...)):
    """Post Request to create a new book"""
    result = None
    if not all(key in new_book for key in ("title", "author", "category")):
        return {"error": "missing key"}
    else:
        insert_book = db.search(
            ~(where("title").matches(new_book["title"], flags=re.IGNORECASE))
        )

    if insert_book:
        result = db.insert(new_book)
    else:
        return {"error": "book already exists"}

    if result:
        return new_book
    return {"error": "error to create book"}


@router.put("/update_book")
async def update_book_route(update_data: dict = Body(...)):
    """Put Request to update a book"""
    filtro = where("title").matches(update_data["title"], flags=re.IGNORECASE)
    result = None
    existing_books = db.search(filtro)
    db.upsert(update_data, filtro)
    if existing_books:
        result = {"success": "book updated"}
    else:
        result = {"success": "book created"}

    if result:
        return result

    return {"error": "Error updating the book"}


@router.delete("/delete_book/{book_title}")
async def delete_book_route(book_title: str):
    """Delete Request to delete a book"""
    result = None
    delete = db.search(where("title").matches(book_title, flags=re.IGNORECASE))
    if delete:
        result = db.remove(where("title").matches(book_title, flags=re.IGNORECASE))
    else:
        return {"error": "book not found"}

    if result:
        return {"success": "book deleted"}
    return {"error": "error to delete book"}
