from fastapi import APIRouter
from routers.crud import create_document
from database import get_db
from models.entry import EntryCreate

router = APIRouter()

@router.post("/entry")
def create_person(entry: EntryCreate):
    db = get_db()
    inserted_id = create_document(db, 'entries', entry)
    return {"message": "Entry created successfully", "inserted_id": inserted_id}

