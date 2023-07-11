from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from database import connect_to_mongodb
from models import User
import bcrypt

app = FastAPI()

# Connect to MongoDB
db = connect_to_mongodb()

@app.get("/")
async def root():
    return {"message": "server up and running"}

@app.post("/users")
def create_user(user: User):
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt(10)).decode("utf-8")

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

@app.post("/login")
def login(credentials: dict):
    email = credentials.get("email")
    password = credentials.get("password")

    if not email or not password:
        raise HTTPException(status_code=422, detail="Email and password are required")

    # Find the user with the provided email
    user = db.users.find_one({"email": email})

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the password matches
    if bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")