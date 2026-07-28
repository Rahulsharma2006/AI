import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

#   Config DOTEnV File
load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API Error")
client = Groq(api_key=my_api_key)
model="llama-3.3-70b-versatile"
role="user"
prompt="Suggest a Name for My company"
message_system = {
    "role":"system",
    "content":"You Are Brand Name Manger who Suggest me a name for my food brand. name should be in one word only with only one options "
}
#    Tempertaure should be 0 for default
messages = [message_system]
response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=1
)
print(response.choices[0].message.content)