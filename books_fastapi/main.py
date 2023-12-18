"""
Script para executar o módulo FastAPI especificado como argumento do script.
"""
import sys
from typing import Callable
from importlib import import_module
from fastapi import FastAPI
from uvicorn import run


def initialize_app(
    title: str,
    description: str,
    version: str,
    reload: bool,
    configure_routes: Callable[[FastAPI], None],
) -> FastAPI:
    """Inicializa uma instância do FastAPI."""
    app = FastAPI(title=title, description=description, version=version, reload=reload)

    if configure_routes:
        configure_routes(app)
    return app


def main():
    """Executa o módulo FastAPI especificado como argumento do script."""
    if len(sys.argv) != 2:
        print("Use: poetry run start <nome_do_módulo> ou start <nome_do_módulo>")
        sys.exit(1)

    module_name = sys.argv[1]
    full_module_name = f"books_fastapi.apps.{module_name}"

    try:
        module = import_module(full_module_name)
        app_instance = module.app
    except ModuleNotFoundError:
        print(f"Error: Módulo '{full_module_name}' não encontrado.")
        sys.exit(1)

    if not app_instance or not isinstance(app_instance, FastAPI):
        print(f"Error: Módulo '{full_module_name}' não define 'app.'")
        sys.exit(1)

    run(full_module_name + ":app", reload=True)


if __name__ == "__main__":
    main()
