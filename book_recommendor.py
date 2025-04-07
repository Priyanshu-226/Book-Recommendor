from llm_utils import get_similar_books_llm
from serper_api import search_similar_books

def get_recommendations(query, profile=""):
    search_books = search_similar_books(query)
    prompt = f"Given this search result for similar books to '{query}' and user profile '{profile}', suggest 5 relevant books:\n{search_books}"
    response = get_similar_books_llm(prompt)
    return response
