from datetime import datetime
from typing import List, Optional
from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField, IntField
from .user import UserDB
from .person import PersonDB
from pydantic import BaseModel, validator
from bson import ObjectId

class EntryBase(BaseModel):
    user: str
    person: str
    mood: Optional[int]
    creation_date: Optional[datetime]
    statements: Optional[List[str]]

class EntryCreate(EntryBase):
    mood: Optional[int] = None
    creation_date: Optional[datetime] = None
    statements: Optional[List[str]] = None

    # Custom validator to convert ObjectId to string
    @validator('user', 'person')
    def convert_objectid(cls, obj_id):
        return ObjectId(obj_id)

class Entry(EntryBase):
    id: str

class EntryDB(Document):
    user = ReferenceField(UserDB, required=True)
    person = ReferenceField(PersonDB, required=True)
    mood = IntField(required=False)
    creation_date = DateTimeField(default=datetime.utcnow)
    statements = ListField(StringField(), required=False)

    meta = {
        'collection': 'entries',
        'alias': 'default'
    }
