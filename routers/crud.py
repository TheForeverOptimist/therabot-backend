from pymongo.collection import Collection
from bson.objectid import ObjectId
from typing import List, Optional
from pydantic import BaseModel


def get_document_by_id(database, collection_name: str, document_id: str):
    collection = database[collection_name]
    return collection.find_one({"_id": ObjectId(document_id)})

def get_documents_by_user(database, collection_name: str, user_id: str):
    collection = database[collection_name]
    return collection.find({"user": ObjectId(user_id)})

def create_document(database, collection_name: str, document: BaseModel):
    collection = database[collection_name]
    document_dict = document.dict()
    inserted_id = collection.insert_one(document_dict).inserted_id
    return str(inserted_id)

def update_document(database, collection_name: str, document_id: str, update_data: dict):
    collection = database[collection_name]
    updated_document = collection.find_one_and_update(
        {"_id": ObjectId(document_id)},
        {"$set": update_data},
        return_document=True
    )
    return updated_document

def delete_document(database, collection_name: str, document_id: str):
    collection = database[collection_name]
    deleted_document = collection.find_one_and_delete({"_id": ObjectId(document_id)})
    return deleted_document
