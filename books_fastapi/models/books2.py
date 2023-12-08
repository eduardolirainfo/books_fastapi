""" Módulo que contém a classe Book2. """
from pydantic import BaseModel, Field


class Books2:
    """Classe que representa um livro."""

    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, title, author, description, rating, published_date):
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class Books2Request(BaseModel):
    """Classe que representa um livro."""

    title: str = Field(..., min_length=3, max_length=50)
    author: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=1, max_length=100)
    rating: int = Field(..., gt=0, lt=6)
    published_date: int = Field(..., gt=1999, lt=2023)

    class Config:
        """Classe de configuração do Pydantic."""

        json_schema_extra = {
            "example": {
                "title": "Livro 1",
                "author": "Autor 1",
                "description": "Descrição 1",
                "rating": 5,
                "published_date": 2021,
            }
        }
