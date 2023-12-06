"""Biblioteca de livros2

Returns:
    _type: dict
"""
from fastapi import APIRouter, Body
from tinydb import TinyDB

router = APIRouter()

db2 = TinyDB("db2.json", indent=4, sort_keys=True)


class Book2:
    """Classe que representa um livro."""

    title: str
    author: str
    description: str
    rating: float

    def __init__(self, title: str, author: str, description: str, rating: float):
        """Inicializa uma instância de Book."""
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


# Removido para não duplicar os dados
# BOOKS = [
#     Book2(
#         title="The Hobbit",
#         author="J. R. R. Tolkien",
#         description="The Hobbit, or There and Back Again is a children's fantasy novel by English author J. R. R. Tolkien. It was published on 21 September 1937 to wide critical acclaim, being nominated for the Carnegie Medal and awarded a prize from the New York Herald Tribune for best juvenile fiction. The book remains popular and is recognized as a classic in children's literature.",
#         rating=4.5,
#     ),
#     Book2(
#         title="The Lord of the Rings",
#         author="J. R. R. Tolkien",
#         description="The Lord of the Rings is an epic high fantasy novel by the English author and scholar J. R. R. Tolkien. Set in Middle-earth, the world at some distant time in the past, the story began as a sequel to Tolkien's 1937 children's book The Hobbit, but eventually developed into a much larger work.",
#         rating=4.7,
#     ),
#     Book2(
#         title="The Silmarillion",
#         author="J. R. R. Tolkien",
#         description="The Silmarillion is a collection of mythopoeic works by English writer J. R. R. Tolkien, edited and published posthumously by his son, Christopher Tolkien, in 1977, with assistance from Guy Gavriel Kay, who later became a noted fantasy writer.",
#         rating=4.6,
#     ),
# ]

# db2.insert_multiple([book.__dict__ for book in BOOKS])


@router.get("/")
async def read_all_books():
    """Return all books."""
    return db2.all()


@router.post("/create-book")
async def create_book(book_request=Body(...)):
    """Create a new book."""
    db2.insert(book_request)
    return db2.all()
