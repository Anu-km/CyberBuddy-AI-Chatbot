from flask_limiter import Limiter
from flask import request, jsonify

BLOCKED = ["ignore previous", "system prompt", "act as"]

def validate_input(msg):
    if len(msg) > 2000:
        return "Message too long"
    if any(b in msg.lower() for b in BLOCKED):
        return "Suspicious input detected"
    return None
