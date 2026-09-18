from flask import Blueprint, request, jsonify
from groq import Groq
import os
from memory import add_message, get_memory
from dotenv import load_dotenv

load_dotenv()

chat_bp = Blueprint("chat", __name__)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = "You are a helpful cybersecurity assistant. Remember conversation context."

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    user = data.get("user", "guest")
    msg = data.get("message", "").strip()

    if not msg:
        return jsonify({"reply": "Please send a message."}), 400

    add_message(user, "user", msg)
    history = get_memory(user)

    context_messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    for m in history:
        context_messages.append({
            "role": m["role"],
            "content": m["content"]
        })

    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=context_messages,
            temperature=0.7,
            max_tokens=512
        )

        reply = completion.choices[0].message.content

        add_message(user, "assistant", reply)
        return jsonify({"reply": reply})

    except Exception as e:
        print("GROQ ERROR:", e)
        return jsonify({"error": str(e)}), 500
