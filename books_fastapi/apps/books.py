"""Biblioteca de livros 

Returns:
    _type: dict
"""
from ..routes import books_router
from ..main import initialize_app

app = initialize_app(
    title="Books API",
    description="API para gerenciar uma biblioteca de livros",
    version="1.0.0",
    reload=True,
    configure_routes=lambda app: app.include_router(
        books_router, prefix="/api/v1/books", tags=["books"]
    ),
)
