from fastapi import APIRouter
from models.person import PersonCreate
from routers.crud import create_document
from database import get_db

router = APIRouter()

@router.post("/person")
def create_person(person: PersonCreate):
    db = get_db()
    inserted_id = create_document(db, 'persons', person)
    return {"message": "Person created successfully", "inserted_id": inserted_id}