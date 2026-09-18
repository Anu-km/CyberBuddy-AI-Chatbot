from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from groq import Groq

from sockets import socketio
from auth import auth_bp
from files import files_bp
from vision import vision_bp
from chat import chat_bp

load_dotenv()

print("GROQ_API_KEY loaded:", bool(os.getenv("GROQ_API_KEY")))
print("OPENAI_API_KEY loaded:", bool(os.getenv("OPENAI_API_KEY")))
print("VIRUSTOTAL_API_KEY loaded:", bool(os.getenv("VIRUSTOTAL_API_KEY")))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("JWT_SECRET", "dev_secret")
CORS(app, supports_credentials=True)

# Configure Groq
GROQ_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_KEY:
    raise RuntimeError("GROQ_API_KEY not found. Check your .env file.")

groq_client = Groq(api_key=GROQ_KEY)

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(files_bp, url_prefix="/api/files")
app.register_blueprint(vision_bp, url_prefix="/api")
app.register_blueprint(chat_bp, url_prefix="/api")
socketio.init_app(app, cors_allowed_origins="*")

@app.route("/")
def home():
    return {"status": "CyberBuddy backend running"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    socketio.run(app, host="0.0.0.0", port=port, debug=True)
