# creating table in column struct - how db is going to look like

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


# create table
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True) # while registering I want to check whether another user exists with same email/username, hence the ndex
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)

    todos = relationship("Todos", back_populates="owner")
