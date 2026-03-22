import os
from openai import OpenAI

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("ReadifyAI Started ✅")
print("Type 'exit' to quit\n")

while True:
    text = input("You: ")

    if text.lower() == "exit":
        print("Goodbye 👋")
        break

    # 🔍 Analyze Mode
    if "analyze" in text.lower():
        print("DEBUG: Analyze mode activated")

        prompt = f"""
You are a professional AI news analyzer.

Analyze the text deeply and respond STRICTLY in this format:

Summary: (2 lines)

Tone: (Neutral / Biased / Emotional)

Bias: (Left-leaning / Right-leaning / Neutral)

Clickbait: (Yes / No)

Fake Indicators:
- (bullet points)

Logical Issues:
- (any exaggeration, missing evidence, emotional manipulation)

Verdict: (Likely Real / Suspicious)

Confidence: (percentage like 70%)

Text:
{text}
"""
    else:
        print("DEBUG: Normal mode")
        prompt = text

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an intelligent AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        ai_reply = response.choices[0].message.content

        print("\nAI:", ai_reply)
        print("-" * 40)

    except Exception as e:
        print("ERROR:", e)