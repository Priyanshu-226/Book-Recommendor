from flask import Flask, request, jsonify
from book_recommender import get_recommendations
from dotenv import load_dotenv
import os

# Load API keys from .env
load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Book Recommender API is running!"

@app.route("/recommend", methods=["GET"])
def recommend():
    query = request.args.get("query")
    profile = request.args.get("profile", "")

    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    try:
        recommendations = get_recommendations(query, profile)
        return jsonify({"recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
