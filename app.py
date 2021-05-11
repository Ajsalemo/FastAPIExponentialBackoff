import logging
import random
import time

import sqlalchemy as SA
from fastapi import FastAPI

from config import database_config
from models import Todo

app = FastAPI()
session = database_config()

# Setting the logging configuration to the following:
# format: <LOGLEVEL>: <MESSAGE>
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)


# This function implements a back off reconnection attempt with a maximum of 5 tries before throwing the exception
# This function wraps all queries to catch disconnects and/or unable to connect to database errors
def retry_with_backoff(f, attempts=5, backoff_in_seconds=1):
    while attempts > 0:
        attempts -= 1
        try:
            logging.info("Connecting to Postgres through SQLAlchemy..")
            return f()  # "break" if query was successful and return any results
        except SA.exc.DBAPIError as exc:
            if attempts > 0 and exc.connection_invalidated:
                logging.warning(
                    f"Retry - trying to establish a connection. Attempt {attempts}"
                )
                session.rollback()
                sleep = backoff_in_seconds * 2 ** attempts + random.uniform(0, 1)
                time.sleep(sleep)
            else:
                raise


@app.get("/")
async def root():
    def select_all():
        todo = session.query(Todo).all()
        print(todo)
        return todo

    retry_with_backoff(select_all)
    return {"message": "Hello World"}
