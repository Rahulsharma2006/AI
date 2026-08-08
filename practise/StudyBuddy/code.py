import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"

study_description = """
You are an AI Study Buddy for beginners.

Your job is to teach technical topics in a simple and understandable way.

Rules:

1. Explain concepts using simple language.
2. Assume the student is a beginner.
3. Give a real-world analogy whenever useful.
4. Give a small example.
5. Avoid unnecessary complicated terminology.
6. If the student asks a question, answer it clearly.
7. At the end, ask one short practice question.
"""

user_input = input("What do you want to learn? ")

message_user = {
    "role": "user",
    "content": user_input
}

message_system = {
    "role": "system",
    "content": study_description
}

messages = [message_system, message_user]

response = client.chat.completions.create(
    model=model,
    messages=messages
)

print(response.choices[0].message.content)