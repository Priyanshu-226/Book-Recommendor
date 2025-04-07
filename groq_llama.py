import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json",
}

async def ask_llama(query: str) -> str:
    payload = {
        "model": "llama3-8b-8192",  # or use "llama3-70b-8192" if available
        "messages": [
            {"role": "system", "content": "You are a helpful book recommendation assistant."},
            {"role": "user", "content": query}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GROQ_URL, json=payload, headers=HEADERS)
        data = response.json()

    return data["choices"][0]["message"]["content"]
