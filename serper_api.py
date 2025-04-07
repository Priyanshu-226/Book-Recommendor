import requests
import os

def search_similar_books(query):
    api_key = os.getenv("SERPER_API_KEY")
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": api_key}
    payload = {"q": f"books like {query}"}

    res = requests.post(url, json=payload, headers=headers)
    results = res.json()

    books = []
    for item in results.get("organic", []):
        books.append(item.get("title", ""))
    return books
