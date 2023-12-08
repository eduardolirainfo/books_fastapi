"""Database module, including the database connection and the database"""
import os
from tinydb import TinyDB
from .models.books2 import Books2


def get_database_instance(app_name):
    """Return the database instance."""
    db = TinyDB(f"{app_name}.json", sort_keys=True, indent=4)
    if os.path.isfile(f"{app_name}.json") and os.stat(f"{app_name}.json").st_size == 0:
        if app_name == "db":
            books_create = [
                {
                    "title": "The Hound of the Baskervilles",
                    "author": "Conan Doyle",
                    "category": "mystery",
                    "published_date": 1902,
                },
                {
                    "title": "The War of the Worlds",
                    "author": "H. G. Wells",
                    "category": "science fiction",
                    "published_date": 1898,
                },
                {
                    "title": "Last Days of Pompeii",
                    "author": "Edward Bulwer-Lytton",
                    "category": "historical",
                    "published_date": 1834,
                },
            ]
            db.insert_multiple(books_create)

        elif app_name == "db2":
            books_create2 = [
                Books2(
                    title="The Hobbit",
                    author="J. R. R. Tolkien",
                    description="The Hobbit, or There and Back Again...",
                    rating=4.5,
                    published_date=1937,
                ),
                Books2(
                    title="The Lord of the Rings",
                    author="J. R. R. Tolkien",
                    description="The Lord of the Rings is an epic high...",
                    rating=4.7,
                    published_date=1954,
                ),
                Books2(
                    title="The Silmarillion",
                    author="J. R. R. Tolkien",
                    description="The Silmarillion is a collection of ...",
                    rating=4.6,
                    published_date=1977,
                ),
            ]
            db.insert_multiple([books2.dict() for books2 in books_create2])
        else:
            raise ValueError(f"App name '{app_name}' not recognized")
    return db
