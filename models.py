from pydantic import BaseModel
from sqlalchemy import Column, Integer

from config import Base


# SQLAlchemy model
class Books(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    book = Column("book")
    author = Column("author")
    description = Column("description")


# FastAPI model for validation 
class BookValidation(BaseModel):
    book: str
    description: str
    author: str
