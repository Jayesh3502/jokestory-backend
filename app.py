from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def health_check():
    return "Backend is up ✅", 200

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    api_key = data.get("apiKey")
    content_type = data.get("type")
    genre = data.get("genre")
    language = data.get("language")

    if not (api_key and content_type and genre and language):
        return jsonify({"error": "Missing fields"}), 400

    prompt = f"Tell me a {genre} {content_type} in {language}."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
        result = model.generate_content(prompt)
        return jsonify({"output": result.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
