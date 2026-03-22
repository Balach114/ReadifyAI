import tkinter as tk
from openai import OpenAI
import os
import threading

# API Key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("NEW UI LOADED ✅")

# =========================
# FUNCTIONS
# =========================

def send_message():
    user_input = entry.get()

    if user_input.strip() == "":
        return

    chat_box.insert(tk.END, "👤 You: " + user_input + "\n")
    entry.delete(0, tk.END)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
               {"role": "user", "content": user_input}
            ]
        )

        ai_reply = response.choices[0].message.content
        chat_box.insert(tk.END, "🤖 AI: " + ai_reply + "\n\n")

    except Exception as e:
        chat_box.insert(tk.END, "ERROR: " + str(e) + "\n\n")

    chat_box.see(tk.END)


def analyze_text():
    user_input = entry.get()

    if user_input.strip() == "":
        return

    chat_box.insert(tk.END, "🧠 Analyze: " + user_input + "\n")
    chat_box.insert(tk.END, "⏳ Analyzing...\n")
    entry.delete(0, tk.END)

    # Run API in separate thread
    threading.Thread(target=process_analysis, args=(user_input,)).start()

def process_analysis(user_input):
    prompt = f"""
Analyze the following text and respond in this format:

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
{user_input}
"""

    try:
        print("Sending request...")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        ai_reply = response.choices[0].message.content

        # Call UI update safely
        window.after(0, display_result, ai_reply)

    except Exception as e:
        window.after(0, chat_box.insert, tk.END, "ERROR: " + str(e) + "\n\n")

def display_result(ai_reply):

    if "Likely Real" in ai_reply:
       color = "lightgreen"
    elif "Suspicious" in ai_reply:
      color = "red"
    else:
     color = "white"

    chat_box.insert(tk.END, "📊 Result:\n", "bold")
    chat_box.insert(tk.END, ai_reply + "\n\n", color)

    chat_box.tag_config("lightgreen", foreground="lightgreen")
    chat_box.tag_config("red", foreground="red")
    chat_box.tag_config("bold", font=("Arial", 11, "bold"))

    chat_box.see(tk.END)        


# =========================
# UI SETUP (DARK MODE)
# =========================

window = tk.Tk()
window.title("ReadifyAI 🤖")
window.geometry("600x500")
window.configure(bg="#1e1e1e")

# Chat box
chat_box = tk.Text(
    window,
    wrap=tk.WORD,
    height=20,
    font=("Arial", 11),
    bg="#2D3748",
    fg="white",
    insertbackground="white"
)
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Bottom frame
frame = tk.Frame(window, bg="#1e1e1e")
frame.pack(pady=5)

# Input field
entry = tk.Entry(
    frame,
    width=50,
    font=("Arial", 12),
    bg="#2D3748",
    fg="white",
    insertbackground="white"
)
entry.pack(side=tk.LEFT, padx=5)

# Send button
send_button = tk.Button(
    frame,
    text="Send",
    command=send_message,
    bg="#2568FB",
    fg="white"
)
send_button.pack(side=tk.LEFT, padx=5)

# Analyze button
analyze_button = tk.Button(
    frame,
    text="Analyze",
    command=analyze_text,
    bg="#A239EA",
    fg="white"
)
analyze_button.pack(side=tk.LEFT)

# Enter key support
window.bind("<Return>", lambda event: send_message())

# Run app
window.mainloop()