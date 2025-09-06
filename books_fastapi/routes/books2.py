<<<<<<< HEAD
"""Biblioteca de livros2

Returns:
    _type: dict
"""
from fastapi import APIRouter, HTTPException, Path, Query
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from tinydb import where
from ..models.books2 import Books2Request
from ..database import get_database_instance


router = APIRouter()

db = get_database_instance("db2")


@router.get("/" , status_code=HTTP_200_OK)
async def read_all_books():
    """Return all books."""
    return db.all()


@router.get("/{book_id}", status_code=HTTP_200_OK)
async def read_book_by_id(book_id: int = Path(..., gt=0)):
    """Return a book by id."""
    book = db.get(doc_id=book_id)
    if book:
        return book
    raise HTTPException(status_code=404, detail="Book not found")


@router.get("/byrating/")
async def read_book_by_rating(book_rating: int = Query(..., gt=0, lt=6)):
    """Return a book by rating."""
    result = db.search(where("rating") == book_rating)
    if result:
        return result
    return {"error": "Rating not found"}


@router.get("/published/", status_code=HTTP_200_OK)
async def read_book_by_published_date(book_published_date: int = Query(..., gt=1999, lt=2031)):
    """Return a book by published date."""
    result = db.search(where("published_date") == book_published_date)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Book not found")


@router.post("/create-book", status_code=HTTP_201_CREATED)
async def create_book(book_request: Books2Request):
    """Create a new book."""
    new_book = book_request.model_dump()    
    filter_title = where("title") == book_request.title
    existing_books = db.search(filter_title)
    
    if existing_books:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Book already exists")
    
    new_book_id = db.insert(new_book)
 
    if new_book_id:
        return db.get(doc_id=new_book_id)
    
    return HTTP_400_BAD_REQUEST


@router.put("/update-book", status_code=HTTP_204_NO_CONTENT)
async def update_book(book_request: Books2Request):
    """Update a book."""
    filter_title = where("title") == book_request.title
    detail = None
    existing_books = db.search(filter_title)
    db.upsert(book_request.model_dump(), filter_title)
    if existing_books:
        detail = "Book updated"
    else:
        detail = "Book not found"

    if detail:
        raise HTTPException(status_code=200, detail=detail)

    raise HTTPException(status_code=400, detail="Error updating the book")


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
=======
"""Biblioteca de livros2

Returns:
    _type: dict
"""
from fastapi import APIRouter, HTTPException, Path, Query
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
async def read_book_by_id(book_id: int = Path(..., gt=0)):
    """Return a book by id."""
    book = db.get(doc_id=book_id)
    if book:
        return book
    raise HTTPException(status_code=404, detail="Book not found")


@router.get("/byrating/")
async def read_book_by_rating(book_rating: int = Query(..., gt=0, lt=6)):
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
    raise HTTPException(status_code=404, detail="Book not found")


@router.post("/create-book")
async def create_book(book_request: Books2Request):
    """Create a new book."""
    new_book = book_request.model_dump()
    
    if db.search(where("title") == book_request.title):
        raise HTTPException(status_code=400, detail="Book already exists")
    
    if db.insert(new_book):
        raise HTTPException(status_code=201, detail="Book created")
    
    raise HTTPException(status_code=400, detail="Error creating the book")


@router.put("/update-book")
async def update_book(book_request: Books2Request):
    """Update a book."""
    filter_title = where("title") == book_request.title
    detail = None
    existing_books = db.search(filter_title)
    db.upsert(book_request.model_dump(), filter_title)
    if existing_books:
        detail = "Book updated"
    else:
        detail = "Book not found"

    if detail:
        raise HTTPException(status_code=200, detail=detail)

    raise HTTPException(status_code=400, detail="Error updating the book")


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
>>>>>>> 292115e6c566942eceb643cb6ade117c58a19160
