from datetime import datetime
from db import logs

def log_event(user, msg, reply):
    logs.insert_one({
        "user": user,
        "prompt": msg,
        "reply": reply,
        "time": datetime.utcnow()
    })
