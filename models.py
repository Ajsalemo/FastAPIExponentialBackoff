from sqlalchemy import Column, Integer

from config import Base


class Books(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    book = Column("book")
    author = Column("author")
    description = Column("description")
