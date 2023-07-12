from fastapi import APIRouter, Header, Depends
from fastapi.exceptions import HTTPException
from models.person import PersonCreate
from routers.crud import create_document, get_documents_by_user, get_document_by_id, update_document
from clients.database import get_db
from utils import CustomJSONEncoder
from models.person import PersonBase
import json
from typing import List

router = APIRouter()

@router.post("/person")
def create_person(person: PersonCreate):
    db = get_db()
    inserted_id = create_document(db, 'persons', person)
    return {"message": "Person created successfully", "inserted_id": inserted_id}


@router.get("/person/me")
def get_user_entries(user_id: str = Header(...), db=Depends(get_db)):
    persons = get_documents_by_user(db, 'persons', user_id)
    response_content = {
        "user_id": user_id,
        "persons": list(persons)
    }
    return json.loads(json.dumps(response_content, cls=CustomJSONEncoder))

@router.get("/person/{id}")
def get_entry(id: str, db=Depends(get_db)):
    person = get_document_by_id(db, 'persons', id)
    if person:
        return json.loads(json.dumps(person, cls=CustomJSONEncoder))
    else:
        raise HTTPException(status_code=404, detail="Person not found")

@router.patch("/person/{id}")
def update_person(id: str, update_data: dict, db=Depends(get_db)):
    summary = update_data.get('summary')
    if summary is not None:
        person = get_document_by_id(db, 'persons', id)
        if person:
            current_summary = person.get('summary', [])
            updated_summary = current_summary + [summary]
            update_data['summary'] = updated_summary
    updated_document = update_document(db, 'persons', id, update_data)
    if updated_document:
        return {"message": "Person updated successfully"}
    return {"message": "Person not found"}






