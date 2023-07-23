from datetime import datetime
from typing import List, Optional
from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField
from .user import UserDB
from pydantic import BaseModel, validator
from bson import ObjectId

class PersonBase(BaseModel):
    user: str
    name: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    summary: Optional[List[str]]

class PersonCreate(PersonBase):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    summary: List[str] = []

    # Custom validator to convert ObjectId to string
    @validator('user')
    def convert_objectid(cls, user):
        if isinstance(user, ObjectId):
            return user
        return ObjectId(user)

class Person(PersonBase):
    id: str

class PersonDB(Document):
    user = ReferenceField(UserDB, required=True)
    name = StringField(required=True)
    start_date = DateTimeField(required=False)
    end_date = DateTimeField(required=False)
    summary = ListField(StringField(), required=False)

    meta = {
        'collection': 'persons',
        'alias': 'default'
    }
