""" Módulo que contém a classe Book2. """
from pydantic import BaseModel, Field


class Books2:
    """Classe que representa um livro."""

    title: str
    author: str
    description: str
    rating: int

    def __init__(self, title, author, description, rating):
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class Books2Request(BaseModel):
    """Classe que representa um livro."""

    title: str = Field(..., min_length=3, max_length=50)
    author: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=1, max_length=100)
    rating: int = Field(..., gt=0, lt=6)
