from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    text = data.get("text")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": text}]
    )

    return jsonify({"result": response.choices[0].message.content})


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text")
    mode = data.get("mode")

    # 🔥 MULTI-MODE SYSTEM
    if mode == "news":
        prompt = f"""
        Analyze this news:

        {text}

        Give:
        - Summary
        - Is it fake or real?
        - Bias
        - Red flags
        """

    elif mode == "ai_detection":
        prompt = f"""
        Detect if AI generated:

        {text}

        Give:
        - Probability (%)
        - Reasons
        """

    elif mode == "claim":
        prompt = f"""
        Verify this claim:

        {text}

        Give:
        - True / False / Unverified
        - Explanation
        """

    else:
        # default text analysis
        prompt = f"""
        Analyze this text:

        {text}

        Provide:
        - Summary
        - Tone
        - Bias
        - Verdict
        """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return jsonify({"result": response.choices[0].message.content})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
