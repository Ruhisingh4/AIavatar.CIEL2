# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

print("🔥 Running NEW avatar.py")

import os
import time
from flask import Flask, render_template, request, jsonify

# Flask app
app = Flask(__name__)

# Load API key
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
print("DEBUG: Loaded API KEY =", str(OPENAI_KEY)[:10], "********")

# Import new OpenAI client
try:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_KEY)
except Exception as e:
    print("OpenAI import error:", e)
    client = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.json or {}
    q = data.get("question", "").strip()

    if not q:
        return jsonify({"ok": False, "answer": "Please ask a question."})

    # If OpenAI client is ready
    if client and OPENAI_KEY:
        try:
            time.sleep(1)  # avoid rate limit spam

            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional AI presenter who explains clearly."
                    },
                    {"role": "user", "content": q}
                ]
            )

            # ✅ NEW API FORMAT — this is the correct way
            answer = resp.choices[0].message.content

            return jsonify({"ok": True, "answer": answer})

        except Exception as e:
            print("OpenAI error:", e)
            return jsonify({"ok": False, "answer": "AI limit reached. Try again in 10 seconds."})

    # fallback response
    return jsonify({
        "ok": True,
        "answer": f"I heard: {q}. Add OPENAI_API_KEY to enable full AI."
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
