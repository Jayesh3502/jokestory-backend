from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import openai
import anthropic

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def health_check():
    return "Backend is up ✅", 200

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    llm = data.get("llm")
    api_key = data.get("apiKey")
    content_type = data.get("type")
    genre = data.get("genre")
    language = data.get("language")

    if not (llm and api_key and content_type and genre and language):
        return jsonify({"error": "Missing fields"}), 400

    prompt = f"Tell me a {genre} {content_type} in {language}."

    try:
        if llm == "gemini":
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-pro")
            result = model.generate_content(prompt)
            return jsonify({"output": result.text})

        elif llm == "openai":
            openai.api_key = api_key
            result = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            return jsonify({"output": result.choices[0].message["content"]})

        elif llm == "claude":
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            return jsonify({"output": response.content[0].text})

        else:
            return jsonify({"error": "Unsupported LLM"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
