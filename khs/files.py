from flask import Blueprint, request, jsonify
import pdfplumber
from PIL import Image
import os
import requests
from urlhaus_checker import check_urlhaus

files_bp = Blueprint("files", __name__)

@files_bp.route("/parse", methods=["POST"])
def parse_file():
    file = request.files["file"]

    if file.filename.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            text = "\n".join(p.extract_text() or "" for p in pdf.pages)
    elif file.filename.endswith(".txt"):
        text = file.read().decode()
    else:
        text = "Image uploaded (vision can be added)"

    return jsonify({"content": text[:4000]})

@files_bp.route("/vt/scan", methods=["POST"])
def virustotal_scan():
    data = request.json or {}
    file_hash = data.get("hash")
    if not file_hash:
        return jsonify({"error": "Missing hash in request JSON (e.g. {\"hash\": \"<sha256|md5|sha1>\"})"}), 400

    api_key = os.getenv("VIRUSTOTAL_API_KEY")
    if not api_key:
        return jsonify({"error": "VIRUSTOTAL_API_KEY not configured in environment"}), 500

    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {"x-apikey": api_key}

    resp = requests.get(url, headers=headers, timeout=20)
    if resp.status_code != 200:
        return jsonify({"error": "VirusTotal query failed", "status_code": resp.status_code, "detail": resp.text}), resp.status_code

    payload = resp.json()

    # return concise data
    result = {
        "id": payload.get("data", {}).get("id"),
        "type": payload.get("data", {}).get("type"),
        "attributes": payload.get("data", {}).get("attributes", {})
    }

    return jsonify(result)

@files_bp.route("/abuseipdb/check", methods=["POST"])
def abuseipdb_check():
    data = request.json or {}
    ip = data.get("ip")
    if not ip:
        return jsonify({"error": "Missing ip in request JSON (e.g., {\"ip\": \"8.8.8.8\"})"}), 400

    api_key = os.getenv("ABUSEIPDB_API_KEY")
    if not api_key:
        return jsonify({"error": "ABUSEIPDB_API_KEY not configured in environment"}), 500

    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Accept": "application/json",
        "Key": api_key
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    resp = requests.get(url, headers=headers, params=params, timeout=20)
    if resp.status_code != 200:
        return jsonify({"error": "AbuseIPDB lookup failed", "status_code": resp.status_code, "detail": resp.text}), resp.status_code

    return jsonify(resp.json())

@files_bp.route("/otx/ip", methods=["POST"])
def otx_ip_lookup():
    data = request.json or {}
    ip = data.get("ip")
    if not ip:
        return jsonify({"error": "Missing ip in request JSON (e.g., {\"ip\": \"8.8.8.8\"})"}), 400

    api_key = os.getenv("OTX_API_KEY")
    if not api_key:
        return jsonify({"error": "OTX_API_KEY not configured in environment"}), 500

    url = f"https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/general"
    headers = {
        "X-OTX-API-KEY": api_key,
        "Accept": "application/json"
    }

    resp = requests.get(url, headers=headers, timeout=20)
    if resp.status_code != 200:
        return jsonify({"error": "OTX IP lookup failed", "status_code": resp.status_code, "detail": resp.text}), resp.status_code

    return jsonify(resp.json())

@files_bp.route("/urlhaus/check", methods=["POST"])
def urlhaus_check():
    data = request.json or {}
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing url in request JSON (e.g. {\"url\": \"http://example.com\"})"}), 400

    result = check_urlhaus(url)
    if result.get("status") == "malicious":
        return jsonify({"alert": "🚨 Malicious URL detected!", "details": result})

    return jsonify({"alert": "✅ Safe URL", "details": result})
@files_bp.route("/api/files/analyze", methods=["POST"])
def analyze_threat_route():
    from security_engine import analyze_threat

    data = request.json or {}
    ip = data.get("ip")
    url = data.get("url")

    result = analyze_threat(ip, url)
    return jsonify(result)
@files_bp.route("/shodan/host", methods=["POST"])
def shodan_host_lookup():
    data = request.json or {}
    ip = data.get("ip")
    if not ip:
        return jsonify({"error": "Missing ip in request JSON (e.g., {\"ip\": \"8.8.8.8\"})"}), 400

    api_key = os.getenv("SHODAN_API_KEY")
    if not api_key:
        return jsonify({"error": "SHODAN_API_KEY not configured in environment"}), 500

    url = f"https://api.shodan.io/shodan/host/{ip}"
    params = {"key": api_key}

    resp = requests.get(url, params=params, timeout=20)
    if resp.status_code != 200:
        return jsonify({"error": "Shodan host lookup failed", "status_code": resp.status_code, "detail": resp.text}), resp.status_code

    return jsonify(resp.json())

@files_bp.route("/ismalicious/check", methods=["POST"])
def ismalicious_check():
    data = request.json or {}
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing url in request JSON (e.g., {\"url\": \"http://example.com\"})"}), 400

    api_key = os.getenv("ISMALICIOUS_API_KEY")
    api_secret = os.getenv("ISMALICIOUS_API_SECRET")
    if not api_key or not api_secret:
        return jsonify({"error": "ISMALICIOUS_API_KEY and ISMALICIOUS_API_SECRET must be configured"}), 500

    ismalicious_api = "https://api.ismalicious.com/v1/url/check"
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": api_key,
        "X-API-SECRET": api_secret
    }
    payload = {"url": url}

    try:
        resp = requests.post(ismalicious_api, headers=headers, json=payload, timeout=20)
    except requests.RequestException as exc:
        return jsonify({"error": "ismalicious request failed", "detail": str(exc)}), 502

    if resp.status_code != 200:
        return jsonify({"error": "ismalicious lookup failed", "status_code": resp.status_code, "detail": resp.text}), resp.status_code

    result = resp.json()
    status = result.get("status", "unknown")
    note = "🚨 Malicious URL detected!" if status == "malicious" else "✅ Safe URL"

    return jsonify({"alert": note, "details": result})
