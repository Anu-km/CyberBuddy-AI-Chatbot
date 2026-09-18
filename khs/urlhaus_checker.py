import requests


def check_urlhaus(url_input):
    api = "https://urlhaus-api.abuse.ch/v1/url/"

    payload = {
        "url": url_input
    }

    try:
        response = requests.post(api, data=payload, timeout=20)
        response.raise_for_status()
        result = response.json()

        if result.get("query_status") == "ok":
            return {
                "status": result.get("url_status"),
                "threat": result.get("threat"),
                "host": result.get("host")
            }
        else:
            return {"status": "unknown", "message": result.get("query_status")}

    except requests.RequestException as e:
        return {"error": str(e)}
