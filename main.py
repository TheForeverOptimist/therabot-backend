from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from clients.database import db
from clients.openai import test_openai_connection
from models.user import LoginCredentials, UserCreate
from routers.person_router import router as person_router
from routers.entry_router import router as entry_router
from routers.user_router import router as user_router
from routers.ai_llm_router import router as ai_llm_router
import bcrypt


app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(person_router)
app.include_router(entry_router)
app.include_router(user_router)
app.include_router(ai_llm_router)


app.state.db = db

# Test OpenAI connection
if test_openai_connection():
    print("Connection to OpenAI API is successful!")
else:
    print("Connection to OpenAI API failed")



@app.get("/")
async def root():
    return {"message": "server up and running"}

@app.post("/signup")
def signup(credentials: UserCreate):
    email = credentials.email
    password = credentials.password
    name = credentials.name
    year_of_birth = credentials.year_of_birth

    if not email or not password:
        raise HTTPException(status_code=422, detail="Email and password are required")
    
    #check if email already exists
    existing_user = db.users.find_one({"email": email})
    if existing_user:
        raise HTTPException(status_code=409, detail="User with this email already exists")
    
    #generate a password hash using bcrypt
    # salt = bcrypt.gensalt()
    # hashed_password = bcrypt.hashpw(password, salt)


    #Create a new user record in the database
    new_user = {
        "email": email,
        "password": password,
        "name": name,
        "year_of_birth": year_of_birth
    }
    user_id = db.users.insert_one(new_user).inserted_id

    return {"message": "Signup successful", "user_id" : str(user_id)}

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
        return {"message": "Login successful", "user_id": f"{user['_id']}", "name": f"{user['name']}"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

