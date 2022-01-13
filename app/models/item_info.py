from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base
from sqlalchemy.orm import relationship


class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    # to query by item_name
    item_name = Column(String(45), unique=True, index=True)
    price = Column(Float)

    carts = relationship("Carts", back_populates="cart_item")
