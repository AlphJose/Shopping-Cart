from pydantic import BaseModel, Field
from typing import Optional


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str


