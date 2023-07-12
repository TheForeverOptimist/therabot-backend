from fastapi import APIRouter, Request, Depends, Header
from fastapi.exceptions import HTTPException
from clients.database import get_db
from bson.objectid import ObjectId
from .entry_router import create_entry
from models.entry import EntryCreate
from utils import CustomJSONEncoder
import json
import openai


router = APIRouter()

@router.post("/ai/test")
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
ENTRY_PROMPT_GUIDELINES = """
Mood:{entry.mood} out of 5 (1 being unhappy, and 5 being happy).

Rewrite and summarize these statements for me, written in first person. 
Try to start your response with either "I" or a person's name.

Statements:
"""


@router.post("/ai/entry")
def create_entry_with_ai(entry:EntryCreate):
    # Retrieve related entries from the database
    
    # Generate summary using OpenAI
    prompt = ENTRY_PROMPT_GUIDELINES + str(entry.statements)
    print(prompt)
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,  # Adjust the value based on your desired summary length
        temperature=0.7,
        n=1,
        stop=None
    )

    entry.reflection = response.choices[0].text.strip()
    db_entry = create_entry(entry)
    print(db_entry)
    return entry.reflection



# Prompt guidelines for generating the summary
SUMMARY_PROMPT_GUIDELINES = """
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
    prompt = SUMMARY_PROMPT_GUIDELINES + str(statements)
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



