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
def retry_with_backoff(f):
    attempts = 0
    backoff_in_seconds = 1
    while attempts < 5:
        attempts += 1
        try:
            logging.info("Connecting to Postgres through SQLAlchemy..")
            return f()  # "break" if query was successful and return any results
        except SA.exc.DBAPIError as exc:
            if attempts < 5 and exc.connection_invalidated:
                session.rollback()
                sleep = backoff_in_seconds * 2 ** attempts + random.uniform(0, 1)
                # Rounding the elapsed time to a whole number
                elapsed_time = round(sleep)
                logging.warning(
                    f" Retry - trying to establish a connection. Attempt {attempts} - elapsed time: {elapsed_time} seconds"
                )
                time.sleep(sleep)
            else:
                logging.error("Unable to connect to the database.")
                raise


@app.get("/")
async def root():
    def select_all():
        todo = session.query(Todo).all()
        for t in todo:
            print(t.name)

    retry_with_backoff(select_all)
    return {"message": "Hello World"}
