from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(200), unique=True, index=True)
    # while registering need to check whether another user exists with same email/username, hence the index
    username = Column(String(45), unique=True, index=True)
    first_name = Column(String(45))
    last_name = Column(String(45))
    hashed_password = Column(String(200))

    carts = relationship("Carts", back_populates="owner")
