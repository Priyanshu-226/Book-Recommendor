import os
import asyncio
from dotenv import load_dotenv
from groq_llama import ask_llama

# Load API key
load_dotenv()

def get_user_input():
    query = input("📚 Enter a book name: ")
    profile = input("👤 Optional: Describe your reading preferences (or leave blank): ")
    return query, profile

async def main():
    query, profile = get_user_input()

    if not query:
        print("⚠️  Book query is required.")
        return

    prompt = f"Suggest 5 similar books to '{query}' based on the user's preferences: {profile}"
    print("\n⏳ Fetching recommendations...\n")

    try:
        response = await ask_llama(prompt)
        print("✅ Book Recommendations:\n")
        print(response)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
