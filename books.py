"""biblioteca de livros

Returns:
    _type: dict
"""
import re
from fastapi import Body, FastAPI
from tinydb import TinyDB, Query

app = FastAPI()


db = TinyDB("db.json", indent=4, sort_keys=True)

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
#         {
#              "title": "The Dark World",
#              "author": "Henry Kuttner",
#              "category": "fantasy"
#        },
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
#         {
#             "title": "The Odyssey",
#             "author": "Homer",
#             "category": "historical"
#        },
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
    book_title = book_title.strip()
    result = db.search(
        busca.title.matches(f".*{re.escape(book_title)}.*", flags=re.IGNORECASE)
    )
    if result:
        return result

    return {"error": "book not found"}


@app.get("/api/v1/books/")
async def read_category_by_query(book_category: str):
    """return book by category"""
    book_category = book_category.strip()
    result = db.search(
        busca.category.matches(f".*{re.escape(book_category)}.*", flags=re.IGNORECASE)
    )
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
    result = None
    insert_book = db.search(
        ~(busca.title.matches(new_book["title"], flags=re.IGNORECASE))
    )
    if insert_book:
        result = db.insert(new_book)
    else:
        return {"error": "book already exists"}

    if result:
        return new_book
    return {"error": "error to create book"}


@app.put("/api/v1/books/update_book")
async def update_book(update_book: dict = Body(...)):
    """Put Request to update a book"""
    result = None
    update = db.search(busca.title.matches(update_book["title"], flags=re.IGNORECASE))
    if update:
        result = db.update(update_book, busca.title == update_book["title"])
    else:
        return {"error": "book not found"}

    if result:
        return update_book
    return {"error": "error to update book"}
