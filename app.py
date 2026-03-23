from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Analyze route
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data["text"]

    prompt = f"Analyze this:\n{text}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return jsonify({"result": response.choices[0].message.content})

# 🔥 ADD THIS HERE (NEW)
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    text = data["text"]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": text}]
    )

    return jsonify({"result": response.choices[0].message.content})

# Run app
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port) 