import os
import json
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

# Pydantic Schema
class Ticket(BaseModel):
    name: str
    email: str
    issue: str

# Generate JSON Schema
schema = Ticket.model_json_schema()

# System Prompt
system_prompt = f"""
Extract the personal information from the ticket.

Return ONLY a valid JSON object that strictly follows this JSON Schema.

JSON Schema:
{schema}
"""

# Load Environment Variables
load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Initialize Groq Client
client = Groq(api_key=my_api_key)

model = "llama-3.3-70b-versatile"

prompt = (
    "Hello, My name is Rahul. "
    "I have an iPhone which is not working. "
    "Please mail me on abx@gmail.com."
)

messages = [
    {
        "role": "system",
        "content": system_prompt,
    },
    {
        "role": "user",
        "content": prompt,
    },
]

# API Call
response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0,
    response_format={"type": "json_object"},
)

# Model Response
answer = response.choices[0].message.content

print("Raw Response:")
print(answer)

# Convert JSON string to Python Dictionary
data = json.loads(answer)

# Validate using Pydantic
ticket = Ticket(**data)

print("\nExtracted Information")
print("---------------------")
print("Name :", ticket.name)
print("Email:", ticket.email)
print("Issue:", ticket.issue)