# Core/openapi_parser.py
import json
import yaml
from pathlib import Path
from urllib.parse import urljoin
import requests

def load_spec_from_path_or_url(spec_path_or_url):
    """
    Accept local path or remote URL, return parsed OpenAPI spec (dict).
    """
    try:
        if str(spec_path_or_url).startswith(("http://", "https://")):
            r = requests.get(spec_path_or_url, timeout=10)
            r.raise_for_status()
            text = r.text
        else:
            text = Path(spec_path_or_url).read_text(encoding="utf-8")
        # Try JSON first, then YAML
        try:
            return json.loads(text)
        except Exception:
            return yaml.safe_load(text)
    except Exception as e:
        raise RuntimeError(f"Failed to load OpenAPI spec: {e}")

def extract_endpoints_from_spec(spec, base_url=None):
    """
    Return list of (method, full_url, operationId) for endpoints found in spec.
    base_url (optional) can override servers[0]['url'].
    """
    paths = spec.get("paths", {})
    servers = spec.get("servers") or []
    server_url = None
    if base_url:
        server_url = base_url
    elif servers:
        server_url = servers[0].get("url")
    else:
        server_url = ""

    endpoints = []
    for p, methods in paths.items():
        for method, details in methods.items():
            if method.lower() not in ("get", "post", "put", "delete", "patch", "head", "options"):
                continue
            op_id = details.get("operationId") or details.get("summary") or ""
            full = urljoin(server_url.rstrip("/") + "/", p.lstrip("/"))
            endpoints.append({
                "method": method.upper(),
                "path": p,
                "url": full,
                "operation": op_id,
                "parameters": details.get("parameters", []),
                "requestBody": details.get("requestBody")
            })
    return endpoints
