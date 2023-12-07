"""Biblioteca de livros2

Returns:
    _type: dict
"""
from ..routes import books2_router
from ..main import initialize_app


app = initialize_app(
    title="Books API 2",
    description="API 2 para gerenciar uma biblioteca de livros",
    version="1.0.0",
    reload=True,
    configure_routes=lambda app: app.include_router(
        books2_router, prefix="/api/v1/books2", tags=["books2"]
    ),
)
