from pydantic import BaseModel


class CreateItem(BaseModel):
    item_name: str
    price: float
