import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_similar_books_llm(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.7,
        messages=[
            {"role": "system", "content": "You are a helpful book recommender."},
            {"role": "user", "content": prompt}
        ]
    )
    content = response["choices"][0]["message"]["content"]
    return [line.strip("-• ") for line in content.split("\n") if line.strip()]
