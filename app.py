import logging
import random
import time

import sqlalchemy as SA
from fastapi import FastAPI

from config import database_config
from models import Books, BookValidation

app = FastAPI()
session = database_config()

# Setting the logging configuration to the following:
# format: <LOGLEVEL>: <MESSAGE>
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)


# This function implements a back off reconnection attempt with a maximum of 5 tries before throwing the exception
# This function wraps all queries to catch disconnects and/or unable to connect to database errors
def retry_with_backoff(f):
    attempts = 0
    backoff_in_seconds = 1
    while attempts < 5:
        attempts += 1
        try:
            return f()  # "break" if query was successful and return any results
        except SA.exc.OperationalError as exc:
            if attempts < 5 and exc:
                session.rollback()
                sleep = backoff_in_seconds * 2 ** attempts + random.uniform(0, 1)
                # Rounding the elapsed time to a whole number
                elapsed_time = round(sleep)
                logging.warning(
                    f" Retry - trying to establish a connection. Attempt {attempts} - Retrying in {elapsed_time} seconds."
                )
                time.sleep(sleep)
            else:
                logging.error("Unable to connect to the database.")
                raise


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/book/find/all")
async def find_all_books():
    async def select_all():
        books = await session.query(Books).all()
        all_books = [
            {
                "id": b.id,
                "book": b.book,
                "description": b.description,
                "author": b.author,
            }
            for b in books
        ]
        return {"results": all_books}

    session.close()
    return retry_with_backoff(select_all)


# Find a todo by ID
@app.get("/api/book/find/{id}")
async def find_book(id: int):
    async def find_by_id():
        r = await session.query(Books).filter_by(id=id).first()
        # Check if the ID exists
        if r is not None:
            book_by_id = {
                "id": r.id,
                "book": r.book,
                "description": r.description,
                "author": r.author,
            }
            return {"results": book_by_id}
        # If no book is found with the ID being passed in through params then display an error
        return {"error": f"No book found with id {id}"}

    session.close()
    return retry_with_backoff(find_by_id)


# Add a book
@app.post("/api/book/add")
async def add_book(book: BookValidation):
    print(book)
    return {"message": "hello"}
