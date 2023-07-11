from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: Optional[int] = Field(None, alias="_id")
    email: str
    password: str
    name: str
    year_of_birth: int
