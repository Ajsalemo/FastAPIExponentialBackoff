from sqlalchemy import Boolean, Column, Integer

from config import Base


class Todo(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True)
    name = Column("name")
    completed = Column("completed", Boolean)
