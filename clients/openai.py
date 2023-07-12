import openai
from dotenv import load_dotenv
import os

load_dotenv()

def setup_openai(api_key):
    openai.api_key = api_key

setup_openai(os.getenv('openai_api_key'))

def test_openai_connection():
    try:
        # Connection test request
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt="Can you see this message? Respond with either Y or N.",
            max_tokens=3,
        )
        return response.choices[0].text.strip() == "Y"
    except Exception:
        return False
