# Reports/api_reporter.py
import json
import html as ihtml
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from colorama import Fore, Style

OUTPUT_DIR = Path("Reports/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def _sev_class(sev: str) -> str:
    s = (sev or "").upper()
    if s == "CRITICAL":
        return "sev-critical"
    if s == "HIGH":
        return "sev-high"
    if s == "MEDIUM":
        return "sev-medium"
    if s == "LOW":
        return "sev-low"
    if s == "INFO":
        return "sev-info"
    return "sev-unknown"

def _section_count(results: Dict[str, List[Dict[str, Any]]]) -> int:
    return sum(len(v) for v in results.values())

def generate_json(results: Dict[str, List[Dict[str, Any]]], cfg: Dict[str, Any]) -> Path:
    path = OUTPUT_DIR / "api_security_report.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    return path

def generate_html(results: Dict[str, List[Dict[str, Any]]], cfg: Dict[str, Any]) -> Path:
    title = cfg.get("report", {}).get("report_header", "Header")
    report_type = cfg.get("report", {}).get("API_report", "API Security Report")
    api_link = cfg.get("API_Scanner", {}).get("base_url", "N/A")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    company = cfg.get("tool_info", {}).get("company_name", "Your Company")
    footer = cfg.get("report", {}).get("report_footer", "Footer")
    year = cfg.get("tool_info", {}).get("year", "2025")
    total = _section_count(results)

    # minimal, focused stylesheet (kept lean)
    css = """
            body{font-family:Arial,Helvetica,sans-serif;background:#111;color:#eee;margin:0;padding:20px}
            .container{max-width:1100px;margin:auto;background:#1f2937;padding:20px;border-radius:10px}
            .header {
                background: #fde047;
                color: #222;
                padding: 14px;
                border-radius: 8px;
                text-align: center;
            }
            .header h1{margin:0;font-size:30px}
            .header h2{margin:4px 0 0 0;font-size:20px;font-weight:normal;color:#333}
            .header h4{margin:4px 0 0 0;font-size:14px;font-weight:normal;color:#333;text-align:right}
            .timestamp{font-size:14px;text-align:right;margin:10px 0 16px 0}
            .section{background:#0f172a;border:1px solid #334155;border-radius:8px;margin:14px 0;overflow:hidden}
            .section-title{margin:0;padding:10px 14px;color:#fff;font-weight:800}
            .zap{background:linear-gradient(90deg,#0ea5e9,#38bdf8)}
            .sth{background:linear-gradient(90deg,#10b981,#34d399)}
            .fuz{background:linear-gradient(90deg,#10b981,#34d399)}
            .card{padding:14px}
            .item{background:#111827;border:1px solid #374151;border-radius:8px;padding:10px;margin:10px 0}
            .k{font-weight:700;color:#e7650f;min-width:120px;display:inline-block}
            code{background:#111;padding:2px 6px;border-radius:4px}
            .sev-badge{font-weight:700;padding:2px 6px;border-radius:6px}
            .sev-critical{background:#fecaca;color:#7f1d1d}
            .sev-high{background:#fee2e2;color:#991b1b}
            .sev-medium{background:#fef3c7;color:#92400e}
            .sev-low{background:#d1fae5;color:#065f46}
            .sev-info{background:#e0e7ff;color:#3730a3}
            .sev-unknown{background:#e5e7eb;color:#374151}
            footer{margin-top:20px;text-align:center;background:#fde047;color:#222;padding:10px;border-radius:6px}
            """

    html = [f"""<!DOCTYPE html>
            <html lang="en"><head>
                <meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
                <title>{title} API Report</title>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
                <style>{css}</style>
            </head>
            <body>
            <div class="container">
                <div class="header">
                    <h1><span style="font-size: 1.5em;">🕵️</span> {title}</h1>
                    <h2>🛡️ {report_type} - Total Findings ({total})</h2>
                    <h4>API Link: {api_link}</h4>
                </div>
                <div class="timestamp">
                    <div>🕒 Report Generated: {timestamp}</div>
                </div>
                """]

    def render_section(section_key: str, section_results: List[Dict[str, Any]], label: str, banner_class: str):
        html.append(f'<div class="section">')
        html.append(f'<div class="section-title {banner_class}">{label} ({len(section_results)})</div>')
        html.append('<div class="card">')
        if not section_results:
            html.append('<div class="item">No findings.</div>')
        for it in section_results:
            sev = _sev_class(it.get("severity",""))
            html.append('<div class="item">')
            html.append(f'<div><span class="k">Severity:</span> <span class="sev-badge {sev}">{ihtml.escape(it.get("severity","UNKNOWN"))}</span></div>')
            if it.get("title"):
                html.append(f'<div><span class="k">Title:</span> {ihtml.escape(it.get("title",""))}</div>')
            if it.get("endpoint"):
                html.append(f'<div><span class="k">Endpoint:</span> {ihtml.escape(it.get("endpoint",""))}</div>')
            if it.get("method"):
                html.append(f'<div><span class="k">Method:</span> {ihtml.escape(it.get("method",""))}</div>')
            if it.get("parameter"):
                html.append(f'<div><span class="k">Parameter:</span> {ihtml.escape(it.get("parameter",""))}</div>')
            if it.get("owasp"):
                html.append(f'<div><span class="k">OWASP:</span> {ihtml.escape(it.get("owasp",""))}</div>')
            if it.get("cwe"):
                html.append(f'<div><span class="k">CWE:</span> {ihtml.escape(str(it.get("cwe","")))}></div>')
            if it.get("description"):
                html.append(f'<div><span class="k">Description:</span> {ihtml.escape(it.get("description",""))}</div>')
            if it.get("evidence"):
                # Truncate long evidence for readability
                ev = it.get("evidence","")
                if isinstance(ev, str) and len(ev) > 1200:
                    ev = ev[:1200] + "..."
                html.append(f'<div><span class="k">Evidence:</span> <code>{ihtml.escape(ev)}</code></div>')
            refs = it.get("references") or []
            if refs:
                html.append('<div><span class="k">References:</span> ' + ", ".join(ihtml.escape(r) for r in refs) + '</div>')
            html.append('</div>')
        html.append('</div></div>')

    render_section("ZAP", results.get("ZAP", []), "<span style=\"font-size:1.25em;\">🕷️</span> OWASP ZAP", "zap")
    # render_section("Schemathesis", results.get("Schemathesis", []), "Schemathesis", "sth")
    render_section("Fuzzer", results.get("Fuzzer", []), "<span style=\"font-size:1.25em;\">💥</span> Custom Fuzzer", "fuz")

    html.append(f"""
                <footer>
                {footer} &middot; © {year} {company}
                </footer>
                </div></body></html>""")

    out = OUTPUT_DIR / "api_security_report.html"
    out.write_text("".join(html), encoding="utf-8")
    return out

def generate_api_reports(results: Dict[str, List[Dict[str, Any]]], cfg: Dict[str, Any]) -> Dict[str, str]:
    """Convenience wrapper: returns paths as strings."""
    report_dir = cfg.get('report_dir', './reports')
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, 'api_security_report.html')
    html_path = generate_html(results, cfg)
    json_path = generate_json(results, cfg)
    print(Fore.LIGHTMAGENTA_EX + f"\n[+] HTML report generated at: {report_path}", flush=True)
    return {"html": str(html_path), "json": str(json_path)}
