import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Postgres environment variables
POSTGRES_USERNAME = os.environ['POSTGRES_USERNAME']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_PORT = os.environ['POSTGRES_PORT']
POSTGRES_HOST = os.environ['POSTGRES_HOST']
POSTGRES_DATABASE = os.environ['POSTGRES_DATABASE']

def database_config():
    # psycopg2
    engine = create_engine(
        f"postgresql://{POSTGRES_USERNAME}@{POSTGRES_HOST}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}.postgres.database.azure.com:{POSTGRES_PORT}/{POSTGRES_DATABASE}",
        # Pre-pings for connections in the pool to ensure that database connectivity is still valid
        # Does the equivalent of sending a SELECT 1
        # https://docs.sqlalchemy.org/en/14/core/pooling.html#disconnect-handling-pessimistic
        pool_pre_ping=True,
        # Sets the max connections in the pool to 128
        pool_size=128
    )
    Session = sessionmaker(bind=engine)
    session = Session()
    # Engine is bound to session - which can then be used to execute queries
    return session
