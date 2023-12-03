"""biblioteca de livros

Returns:
    _type: dict
"""
import re
from fastapi import Body, FastAPI
from tinydb import TinyDB, Query

app = FastAPI()


db = TinyDB("db.json")

# db.insert_multiple(
#     [
#         {
#             "title": "The Hound of the Baskervilles",
#             "author": "Conan Doyle",
#             "category": "mystery",
#         },
#         {
#             "title": "The War of the Worlds",
#             "author": "H. G. Wells",
#             "category": "science fiction",
#         },
#         {
#             "title": "Last Days of Pompeii",
#             "author": "Edward Bulwer-Lytton",
#             "category": "historical",
#         },
#         {
#             "title": "The Count of Monte Cristo",
#             "author": "Alexandre Dumas",
#             "category": "historical",
#         },
#         {
#             "title": "The Time Machine",
#             "author": "H. G. Wells",
#             "category": "science fiction",
#         },
#         {
#             "title": "A Journey into the Center of the Earth",
#             "author": "Jules Verne",
#             "category": "science fiction",
#         },
#         {"title": "The Dark World", "author": "Henry Kuttner", "category": "fantasy"},
#         {
#             "title": "The Wind in the Willows",
#             "author": "Kenneth Grahame",
#             "category": "fantasy",
#         },
#         {
#             "title": "Life On The Mississippi",
#             "author": "Mark Twain",
#             "category": "historical",
#         },
#         {
#             "title": "Childhood",
#             "author": "Lev Nikolayevich Tolstoy",
#             "category": "biography",
#         },
#         {
#             "title": "The Adventures of Tom Sawyer",
#             "author": "Mark Twain",
#             "category": "biography",
#         },
#         {
#             "title": "The Prince and the Pauper",
#             "author": "Mark Twain",
#             "category": "historical",
#         },
#         {
#             "title": "The Adventures of Huckleberry Finn",
#             "author": "Mark Twain",
#             "category": "historical",
#         },
#         {
#             "title": "The Mysterious Island",
#             "author": "Jules Verne",
#             "category": "science fiction",
#         },
#         {
#             "title": "Treasure Island",
#             "author": "Robert Louis Stevenson",
#             "category": "historical",
#         },
#         {"title": "The Odyssey", "author": "Homer", "category": "historical"},
#     ]
# )

busca = Query()


@app.get("/api/v1/books")
async def read_all_books():
    """return all books"""
    return db.all()


@app.get("/api/v1/books/{book_title}")
async def read_book_title(book_title: str):
    """return book by title"""
    # remover espaços em branco do inicio e fim
    book_title = book_title.strip()
    result = db.search(busca.title.matches(book_title, flags=re.IGNORECASE))
    if result:
        return result

    return {"error": "book not found"}


@app.get("/api/v1/books/")
async def read_category_by_query(book_category: str):
    """return book by category"""
    book_category = book_category.strip()
    result = db.search(busca.category.matches(book_category, flags=re.IGNORECASE))
    if result:
        return result
    return {"error": "category not found"}


@app.get("/api/v1/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    """return book by author and category"""
    result = db.search(
        (busca.author.matches(book_author, flags=re.IGNORECASE))
        & (busca.category.matches(category, flags=re.IGNORECASE))
    )

    if result:
        return result
    return {"error": "author or category not found"}


@app.post("/api/v1/books/create_book")
async def create_book(new_book: dict = Body(...)):
    """Post Request to create a new book"""
    body = new_book
    author = db.search(busca.author.matches(body["author"], flags=re.IGNORECASE))
    category = db.search(busca.category.matches(body["category"], flags=re.IGNORECASE))
    if author and category:
        result = db.search((busca.title.matches(body["title"], flags=re.IGNORECASE)))
        if result:
            return {"error": "book already exists"}
        db.insert(body)
        return body
    return {"error": "error to create book"}
