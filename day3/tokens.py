import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY not found!")

client = Groq(api_key=my_api_key)

model = "llama-3.3-70b-versatile"

prompts = [
    "Suggest a Name for My company",
    "Write a 1000 Words Essay on Machine Learning",
    "Explain Time Travel"
]

for prompt in prompts:
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    usage = response.usage

    print(f"Prompt: {prompt}")
    print(f"Prompt Tokens     : {usage.prompt_tokens}")
    print(f"Completion Tokens : {usage.completion_tokens}")
    print(f"Total Tokens      : {usage.total_tokens}")
    print("-" * 50)