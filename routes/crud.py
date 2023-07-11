from pymongo.collection import Collection
from bson.objectid import ObjectId
from typing import List, Optional
from pydantic import BaseModel

def get_document_by_id(collection: Collection, document_id: str):
    return collection.find_one({"_id": ObjectId(document_id)})

def get_documents(collection: Collection, skip: int = 0, limit: int = 100):
    return collection.find().skip(skip).limit(limit)

def create_document(collection: Collection, document: BaseModel):
    document_dict = document.dict()
    inserted_id = collection.insert_one(document_dict).inserted_id
    return str(inserted_id)

def update_document(collection: Collection, document_id: str, document: BaseModel):
    updated_document = collection.find_one_and_update(
        {"_id": ObjectId(document_id)},
        {"$set": document.dict()},
        return_document=True
    )
    return updated_document

def delete_document(collection: Collection, document_id: str):
    deleted_document = collection.find_one_and_delete({"_id": ObjectId(document_id)})
    return deleted_document

