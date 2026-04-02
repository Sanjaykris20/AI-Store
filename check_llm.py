import os
import groq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("Error: GROQ_API_KEY not found in .env")
    exit(1)

try:
    client = groq.Groq(api_key=api_key)
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful AI."},
            {"role": "user", "content": "Reply with 'LLM is successfully connected and working!'. Nothing else."}
        ],
        model="llama-3.1-8b-instant",
    )
    print(chat_completion.choices[0].message.content)
except Exception as e:
    print(f"Error during LLM connection: {e}")
