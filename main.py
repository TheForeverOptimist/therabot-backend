from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from database import connect_to_mongodb
from models.user import LoginCredentials
from routers.person_router import router as person_router
from routers.entry_router import router as entry_router
from routers.user_router import router as user_router
import bcrypt

app = FastAPI()

app.include_router(person_router)
app.include_router(entry_router)
app.include_router(user_router)

# Connect to MongoDB
db = connect_to_mongodb()
app.state.db = db


@app.get("/")
async def root():
    return {"message": "server up and running"}

@app.post("/login")
def login(credentials: LoginCredentials):
    email = credentials.email
    password = credentials.password

    if not email or not password:
        raise HTTPException(status_code=422, detail="Email and password are required")

    user = db.users.find_one({"email": email})

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

