"""
Script para executar o módulo FastAPI especificado como argumento do script.
"""

import sys
from importlib import import_module
from fastapi import FastAPI
from uvicorn import run


def main():
    """Executa o módulo FastAPI especificado como argumento do script"""
    if len(sys.argv) != 2:
        print("Uso: poetry run start <nome_do_módulo>")
        sys.exit(1)

    module_name = sys.argv[1]
    full_module_name = f"books_fastapi.{module_name}"
    module_path = full_module_name.replace(".", "/")

    try:
        module = import_module(full_module_name)
    except ModuleNotFoundError:
        try:
            module = import_module(f"{module_path}.main")
        except ModuleNotFoundError:
            print(f"Error: Módulo '{full_module_name}' não encontrado.")
            sys.exit(1)

    app = getattr(module, "app", None)

    if not app or not isinstance(app, FastAPI):
        print(f"Error: Módulo '{full_module_name}' não define 'app.'")
        sys.exit(1)

    run(full_module_name + ":app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
