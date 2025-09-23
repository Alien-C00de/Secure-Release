# Core/detectors.py
import re

SENSITIVE_KEYWORDS = [
    "password", "pwd", "secret", "token", "api_key", "ssn",
    "creditcard", "card_number", "authorization", "jwt", "private"
]

def detect_status_anomalies(response):
    issues = []
    if response.status_code >= 500:
        issues.append({
            "title": "Server error",
            "description": f"Server returned HTTP {response.status_code}",
            "severity": "MEDIUM"
        })
    return issues

def detect_sensitive_keywords(response):
    issues = []
    body = ""
    try:
        body = response.text.lower()
    except Exception:
        body = ""
    for kw in SENSITIVE_KEYWORDS:
        if kw in body:
            issues.append({
                "title": "Sensitive keyword in response",
                "description": f"Found '{kw}' in response body",
                "severity": "HIGH"
            })
    return issues

def detect_exposed_headers(response):
    issues = []
    headers = response.headers
    if "X-Powered-By" in headers:
        issues.append({
            "title": "Exposed X-Powered-By header",
            "description": f"Server exposes header X-Powered-By: {headers['X-Powered-By']}",
            "severity": "LOW"
        })
    # CORS check
    if headers.get("Access-Control-Allow-Origin") == "*":
        issues.append({
            "title": "Permissive CORS",
            "description": "Access-Control-Allow-Origin is set to '*'",
            "severity": "MEDIUM"
        })
    return issues

def detect_cookie_flags(response):
    issues = []
    set_cookie = response.headers.get("Set-Cookie")
    if set_cookie:
        if "httponly" not in set_cookie.lower():
            issues.append({
                "title": "Cookie without HttpOnly",
                "description": f"Set-Cookie header missing HttpOnly: {set_cookie}",
                "severity": "MEDIUM"
            })
        if "secure" not in set_cookie.lower():
            issues.append({
                "title": "Cookie without Secure",
                "description": f"Set-Cookie header missing Secure: {set_cookie}",
                "severity": "HIGH"
            })
    return issues
