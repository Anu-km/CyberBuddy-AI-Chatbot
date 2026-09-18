import os
import json
import sqlite3
import requests
from datetime import datetime


def init_database(db_path='security_analysis.db'):
    conn = sqlite3.connect(db_path)
    conn.execute('''
    CREATE TABLE IF NOT EXISTS analysis_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        ip TEXT,
        url TEXT,
        failed_logins INTEGER,
        risk_score INTEGER,
        risk_level TEXT,
        action TEXT,
        alert_flags TEXT,
        data TEXT
    )
    ''')
    conn.commit()
    conn.close()


init_database()


def check_ip_abuse(ip):
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Accept": "application/json",
        "Key": os.getenv("ABUSEIPDB_API_KEY")
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    resp = requests.get(url, headers=headers, params=params, timeout=20)
    return {"status_code": resp.status_code, "body": resp.json()}


def check_url_urlhaus(url_input):
    url = "https://urlhaus-api.abuse.ch/v1/url/"
    payload = {"url": url_input}

    resp = requests.post(url, data=payload, timeout=20)
    return {"status_code": resp.status_code, "body": resp.json()}


def check_virustotal(ip):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {"x-apikey": os.getenv("VIRUSTOTAL_API_KEY")}

    resp = requests.get(url, headers=headers, timeout=20)
    return {"status_code": resp.status_code, "body": resp.json()}


def check_otx(ip):
    key = os.getenv("OTX_API_KEY")
    if not key:
        return {"status_code": 500, "body": {"error": "OTX_API_KEY missing"}}

    url = f"https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/general"
    headers = {"X-OTX-API-KEY": key, "Accept": "application/json"}
    resp = requests.get(url, headers=headers, timeout=20)
    return {"status_code": resp.status_code, "body": resp.json()}


def check_shodan(ip):
    key = os.getenv("SHODAN_API_KEY")
    if not key:
        return {"status_code": 500, "body": {"error": "SHODAN_API_KEY missing"}}

    url = f"https://api.shodan.io/shodan/host/{ip}"
    params = {"key": key}
    resp = requests.get(url, params=params, timeout=20)
    return {"status_code": resp.status_code, "body": resp.json()}


def check_ismalicious(url_input):
    key = os.getenv("ISMALICIOUS_API_KEY")
    secret = os.getenv("ISMALICIOUS_API_SECRET")
    if not key or not secret:
        return {"status_code": 500, "body": {"error": "IsMalicious credentials missing"}}

    url = "https://api.ismalicious.com/v1/url/check"
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": key,
        "X-API-SECRET": secret
    }
    resp = requests.post(url, headers=headers, json={"url": url_input}, timeout=20)
    return {"status_code": resp.status_code, "body": resp.json()}


def calculate_risk_score(results, failed_logins=0):
    score = 0
    alerts = []

    # brute-force behavior
    if failed_logins >= 50:
        score += 30
        alerts.append("excessive_failed_logins")
    elif failed_logins >= 20:
        score += 20
    elif failed_logins > 0:
        score += 10

    # abuseipdb confidence
    abuse_score = 0
    abuse_body = (results.get("abuseipdb") or {}).get("body", {})
    if isinstance(abuse_body, dict):
        abuse_score = abuse_body.get("data", {}).get("abuseConfidenceScore", 0) or 0

    if abuse_score > 30:
        score += 35
        alerts.append("abuse_confidence_high")
    elif abuse_score > 10:
        score += 15

    # OTX pulse alerts
    otx_body = (results.get("otx") or {}).get("body", {})
    pulse_count = 0
    if isinstance(otx_body, dict):
        pulse_count = (otx_body.get("pulse_info", {}).get("count") or 0)

    if pulse_count > 0:
        score += 20
        alerts.append("otx_pulses_present")

    # urlhaus lookup
    urlhaus_body = (results.get("urlhaus") or {}).get("body", {})
    if isinstance(urlhaus_body, dict):
        if urlhaus_body.get("query_status") == "ok" and urlhaus_body.get("url_status") == "malicious":
            score += 35
            alerts.append("urlhaus_malicious")
        elif urlhaus_body.get("query_status") == "ok":
            score += 10

    # ismalicious lookup
    ismalicious_body = (results.get("ismalicious") or {}).get("body", {})
    if isinstance(ismalicious_body, dict):
        if ismalicious_body.get("status") == "malicious":
            score += 30
            alerts.append("ismalicious_malicious")

    # VirusTotal (for ip) detection
    vt_body = (results.get("virustotal") or {}).get("body", {})
    if isinstance(vt_body, dict):
        analysis_stats = vt_body.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
        if analysis_stats:
            mal = analysis_stats.get("malicious", 0) or 0
            suspicious = analysis_stats.get("suspicious", 0) or 0
            score += min(40, mal * 2 + suspicious)
            if mal > 0 or suspicious > 0:
                alerts.append("virustotal_malicious")

    score = min(100, score)

    if score > 70:
        level = "High"
        action = "Block"
    elif score > 30:
        level = "Medium"
        action = "Investigate"
    else:
        level = "Low"
        action = "Monitor"

    return {
        "risk_score": int(score),
        "risk_level": level,
        "action": action,
        "alerts": alerts,
        "abuse_confidence": abuse_score,
        "otx_pulse_count": pulse_count
    }


def persist_analysis(ip, url_input, failed_logins, analysis):
    db_path = os.getenv("SECURITY_DB_PATH", "security_analysis.db")
    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT INTO analysis_history (timestamp, ip, url, failed_logins, risk_score, risk_level, action, alert_flags, data) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            datetime.utcnow().isoformat(),
            ip,
            url_input,
            failed_logins,
            analysis.get("risk_score"),
            analysis.get("risk_level"),
            analysis.get("action"),
            json.dumps(analysis.get("alerts", [])),
            json.dumps(analysis)
        )
    )
    conn.commit()
    conn.close()


def analyze_threat(ip, url_input, failed_logins=0):
    results = {}

    if ip:
        results["abuseipdb"] = check_ip_abuse(ip)
        results["virustotal"] = check_virustotal(ip)
        results["otx"] = check_otx(ip)
        results["shodan"] = check_shodan(ip)
    else:
        results["abuseipdb"] = {"error": "Missing IP"}

    if url_input:
        results["urlhaus"] = check_url_urlhaus(url_input)
        results["ismalicious"] = check_ismalicious(url_input)
    else:
        results["urlhaus"] = {"error": "Missing URL"}

    analysis = calculate_risk_score(results, failed_logins=failed_logins)
    results["summary"] = analysis

    # Persist the analysis for timeline/history
    try:
        persist_analysis(ip, url_input, failed_logins, analysis)
    except Exception as e:
        results["persistence_error"] = str(e)

    return results
