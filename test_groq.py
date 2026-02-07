import os
from groq import Groq
from dotenv import load_dotenv
import json

# Load env from .env
load_dotenv('.env')

api_key = os.getenv("GROQ_API_KEY")
print(f"Checking Key: {api_key[:5]}... (Length: {len(api_key) if api_key else 0})")

if not api_key:
    print("Error: GROQ_API_KEY not found.")
    exit(1)

client = Groq(api_key=api_key)

try:
    print("Sending request to Groq...")
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Output JSON."
            },
            {
                "role": "user",
                "content": "Explain why phishing is bad in one sentence. JSON format: { \"explanation\": ... }"
            }
        ],
        response_format={"type": "json_object"},
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    print("Response received:")
    print(completion.choices[0].message.content)

except Exception as e:
    print(f"Error: {e}")
