def analyze(msg):
    if msg.lower().startswith("cve-"):
        return f"Looking up vulnerability {msg}"

    phishing_keywords = ["urgent", "verify", "password"]
    score = sum(k in msg.lower() for k in phishing_keywords)

    if score >= 2:
        return "⚠ Possible phishing detected"

    return None
