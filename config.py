import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# MySQL environment variables
MYSQL_USERNAME = os.environ['MYSQL_USERNAME']
MYSQL_PASSWORD = os.environ['MYSQL_PASSWORD']
MYSQL_PORT = os.environ['MYSQL_PORT']
MYSQL_HOST = os.environ['MYSQL_HOST']
MYSQL_DATABASE = os.environ['MYSQL_DATABASE']

def database_config():
    # MySQL connection string
    engine = create_engine(
        f"mysql://{MYSQL_USERNAME}@{MYSQL_HOST}:{MYSQL_PASSWORD}@{MYSQL_HOST}.mysql.database.azure.com:{MYSQL_PORT}/{MYSQL_DATABASE}",
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
