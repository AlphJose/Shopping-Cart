from sqlalchemy import Boolean, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Carts(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    # is_active = Column(Boolean, default=True)  # becomes False after check-out

    owner = relationship("Users", back_populates="carts")
    cart_item = relationship("Items", back_populates="carts")