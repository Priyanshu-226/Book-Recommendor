import os
import asyncio
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# === Groq LLaMA Logic ===
async def ask_llama(prompt: str) -> str:
    GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful book recommendation assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GROQ_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

# === Serper Search Logic ===
async def search_books_google(query: str):
    if not SERPER_API_KEY:
        return "🔍 SERPER_API_KEY not provided. Skipping Google Search."

    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "q": f"{query} book"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        books = [r["title"] for r in data.get("organic", [])[:5]]
        return "\n".join(f"- {book}" for book in books) or "No search results."

# === Book Recommendor Orchestration ===
async def get_recommendations(book_query: str, user_profile: str = ""):
    llama_prompt = f"Suggest 5 books similar to '{book_query}'. Consider this user profile: {user_profile}"
    print("\n🤖 Getting recommendations from LLaMA...\n")
    llama_response = await ask_llama(llama_prompt)

    print("\n🌐 Getting search results from Google (Serper)...\n")
    google_results = await search_books_google(book_query)

    return {
        "llama_response": llama_response,
        "google_results": google_results
    }

# === CLI Interface ===
def get_user_input():
    print("📘 Book Recommender — Powered by LLaMA & Google Search\n")
    book = input("📚 Enter a book name: ").strip()
    profile = input("👤 Enter your reading preferences (optional): ").strip()
    return book, profile

async def main():
    book, profile = get_user_input()

    if not book:
        print("❌ Please enter a book name.")
        return

    try:
        result = await get_recommendations(book, profile)
        print("\n✅ Recommendations from LLaMA:\n")
        print(result["llama_response"])
        print("\n🔍 Search Results (Google/Serper):\n")
        print(result["google_results"])
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
