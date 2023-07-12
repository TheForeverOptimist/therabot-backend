import openai
from fastapi import APIRouter, Request, Depends, Header
from fastapi.exceptions import HTTPException
from dotenv import load_dotenv
from database import get_db
from bson.objectid import ObjectId
from utils import CustomJSONEncoder
import os
import json

# Load environment variables from .env file
load_dotenv()

router = APIRouter()

def setup_openai(api_key):
    openai.api_key = api_key

setup_openai(os.getenv('openai_api_key'))


try:
    # Connection test request
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Can you see this message? Respond with either Y or N.",
        max_tokens=3,
    )
    print("Connection to OpenAI API is successful!")
    answer = response.choices[0].text.strip()
    if answer == "Y":
        print("Ai Response: Yes")
    else:
        print("Ai Response: No, the prompt that was sent to me cannot be seen")
except Exception as e:
    print("Connection to OpenAI API failed:", str(e))


@router.post("/ai/response")
async def generate_chat_response(request: Request):
    data = await request.json()
    message = data["message"]

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=message,
        max_tokens=50,
        temperature=0.6,
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()


# Prompt guidelines for generating the summary
PROMPT_GUIDELINES = """
Summaries are useful for:
1. Clarifying emotions for the client.
2. Drawing together the main threads of the data.
3. Starting the process of focusing and prioritising ‘scattered’ thoughts and feelings.

Generate a summary that reflects these objectives for the following list of statements made over time:
"""

def get_user_entries_by_person(user_id, person, db):
    collection = db['entries']
    query = {"user": ObjectId(user_id), "person": ObjectId(person)}
    entries = collection.find(query)
    return entries

@router.get("/ai/summary/{person}")
def generate_summary(person: str, user_id: str = Header(...), db=Depends(get_db)):
    # Retrieve related entries from the database
    entries = get_user_entries_by_person(user_id, person, db)
    if entries:
        statements = [entry['statements'] for entry in entries]
    else:
        raise HTTPException(status_code=404, detail="Entry not found")

    # Generate summary using OpenAI
    prompt = PROMPT_GUIDELINES + str(statements)
    print(prompt)
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,  # Adjust the value based on your desired summary length
        temperature=0.6,
        n=1,
        stop=None
    )

    # Return the generated summary
    return response.choices[0].text.strip()



