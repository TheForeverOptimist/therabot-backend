from datetime import datetime
from typing import List, Optional, Tuple
from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField, IntField, DictField, EmbeddedDocumentField
from .user import UserDB
from .person import PersonDB
from pydantic import BaseModel, validator
from bson import ObjectId


class EntryBase(BaseModel):
    user: str
    person: str
    mood: Optional[int]
    creation_date: Optional[datetime]
    statements: List[Tuple[datetime, str]]
    reflection: Optional[str]


class EntryCreate(EntryBase):
    mood: Optional[int] = None
    creation_date: Optional[datetime] = None
    reflection: Optional[str] = None

    # Custom validator to convert ObjectId to string
    @validator('user', 'person')
    def convert_objectid(cls, obj_id):
        if isinstance(obj_id,ObjectId):
            return obj_id
        return ObjectId(obj_id)

class Entry(EntryBase):
    id: str

class EntryDB(Document):
    user = ReferenceField(UserDB, required=True)
    person = ReferenceField(PersonDB, required=True)
    mood = IntField(required=False)
    creation_date = DateTimeField(default=datetime.utcnow)
    statements = ListField(ListField(DateTimeField(required=True), StringField(required=True)))
    reflection = StringField(required=False)

    meta = {
        'collection': 'entries',
        'alias': 'default'
    }
