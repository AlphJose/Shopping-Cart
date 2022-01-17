from pydantic import BaseModel


class CreateCart(BaseModel):
    item_id: int
