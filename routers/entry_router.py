from fastapi import APIRouter, Depends, Header
from fastapi.exceptions import HTTPException
from routers.crud import create_document, get_documents_by_user, get_document_by_id, update_document
from clients.database import db
from models.entry import EntryCreate
from utils import CustomJSONEncoder
import json
from datetime import datetime
router = APIRouter()

@router.post("/entry")
def create_entry(entry: EntryCreate):
    entry.creation_date = datetime.now()
    inserted_id = create_document(db, 'entries', entry)
    return {"message": "Entry created successfully", "inserted_id": inserted_id}

@router.get("/entry/me")
def get_user_entries(user_id: str = Header(...)):
    entries = get_documents_by_user(db, 'entries', user_id)
    response_content = {
        "user_id": user_id,
        "entries": list(entries)
    }
    return json.loads(json.dumps(response_content, cls=CustomJSONEncoder))

@router.get("/entry/{id}")
def get_entry(id: str):
    entry = get_document_by_id(db, 'entries', id)
    if entry:
        return json.loads(json.dumps(entry, cls=CustomJSONEncoder))
    else:
        raise HTTPException(status_code=404, detail="Entry not found")
    
@router.patch("/entry/{id}")
def update_entry(id: str, update_data: dict):
    statements = update_data.get('statements')
    if statements is not None:
        entry = get_document_by_id(db, 'entries', id)
        if entry:
            current_statements = entry.get('statements', [])
            if isinstance(statements, list):
                updated_statements = current_statements + statements
            else:
                updated_statements = current_statements + [statements]
            update_data['statements'] = updated_statements
    updated_document = update_document(db, 'entries', id, update_data)
    if updated_document:
        return {"message": "Entry updated successfully"}
    return {"message": "Entry not found"}

