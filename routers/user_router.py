from fastapi import APIRouter
from clients.database import db
from models.user import UserCreate
import bcrypt

router = APIRouter()

@router.post("/user")
def create_user(user: UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    # Create the user document with the hashed password
    new_user = {
        "email": user.email,
        "password": hashed_password,
        "name": user.name,
        "year_of_birth": user.year_of_birth
    }

    # Get the collection for the User model
    users_collection = db["users"]

    # Insert the new_user document into the users collection
    users_collection.insert_one(new_user)

    return {"message": "User created successfully"}
