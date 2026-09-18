from flask import Blueprint, request, jsonify
from openai import OpenAI
import os

vision_bp = Blueprint("vision", __name__)

def get_client():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not found in environment")
    return OpenAI(api_key=key)

@vision_bp.route("/vision", methods=["POST"])
def vision():
    return jsonify({"reply": "Vision endpoint alive"})
