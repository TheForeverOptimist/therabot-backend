from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from clients.database import connect_to_mongodb
from clients.openai import test_openai_connection
from models.user import LoginCredentials
from routers.person_router import router as person_router
from routers.entry_router import router as entry_router
from routers.user_router import router as user_router
from routers.ai_llm_router import router as ai_llm_router
import bcrypt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(person_router)
app.include_router(entry_router)
app.include_router(user_router)
app.include_router(ai_llm_router)

# Connect to MongoDb
db = connect_to_mongodb()
app.state.db = db

# Test OpenAI connection
if test_openai_connection():
    print("Connection to OpenAI API is successful!")
else:
    print("Connection to OpenAI API failed")



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
        print(user)
        return {"message": "Login successful", "user_id": f"{user['_id']}"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

