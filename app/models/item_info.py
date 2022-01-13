from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base


class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    # to query by itemname
    itemname = Column(String, unique=True, index=True)
    price = Column(Float)
