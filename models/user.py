from pydantic import BaseModel
from typing import Optional
from mongoengine import Document, StringField, IntField

class UserBase(BaseModel):
    email: str
    password: str
    name: str
    year_of_birth: int

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: Optional[str]

class UserDB(Document):
    email = StringField(required=True)
    password = StringField(required=True)
    name = StringField(required=True)
    year_of_birth = IntField(required=True)

    meta = {
        'collection': 'users',
        'alias': 'default'
    }

class LoginCredentials(BaseModel):
    email: str
    password: str



