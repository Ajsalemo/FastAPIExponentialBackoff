import logging
import random
import time

from fastapi import FastAPI

app = FastAPI()

# Setting the logging configuration to the following:
# format: <LOGLEVEL>: <MESSAGE>
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

# This function implements a back off reconnection attempt with a maximum of 5 tries before throwing the exception
def retry_with_backoff(retries=5, backoff_in_seconds=1):
    x = 0
    while True:
        try:
            return logging.info("Connecting..")
        except:
            if x == retries:
                raise
            else:
                sleep = backoff_in_seconds * 2 ** x + random.uniform(0, 1)
                time.sleep(sleep)
                x += 1
                logging.warning(
                    f"Retry - trying to establish a connection. Attempt {x}"
                )

# To be invoked on application startup
retry_with_backoff()


@app.get("/")
async def root():
    return {"message": "Hello World"}
