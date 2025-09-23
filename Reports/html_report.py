import os
import re
import html as ihtml
from datetime import datetime
from colorama import Fore, Style

def render_html(results, config):
    company = config.get("tool_info", {}).get("company_name", "Your Company")
    title = config.get("report", {}).get("report_header", "Header")
    report_type = config.get("report", {}).get("report_title", "Security Report")
    timestamp = datetime.now().strftime("%A %d-%b-%Y %H:%M:%S")
    app_name = config.get("Assessment_Project_Details", {}).get("name", "Project")
    app_version = config.get("Assessment_Project_Details", {}).get("version", "1.0.0")
    app_technology = config.get("Assessment_Project_Details", {}).get("technology", "N/A")
    footer = config.get("report", {}).get("report_footer", "Footer")
    year = config.get("tool_info", {}).get("year", "2025")
    issues = {
        "Secret Scanner": results.get("Secret Scanner", []),
        "Code Analyzer": results.get("Code Analyzer", []),
        "Dependency Scan": results.get("Dependency Scan", [])
    }

    total_findings = sum(len(v) for v in issues.values())

    # 🎨 Modern CSS (taken from api_reporter look)
    css = """body {
                font-family: Arial, Helvetica, sans-serif;
                background: #111;
                color: #eee;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 1100px;
                margin: auto;
                background: #1f2937;
                padding: 20px;
                border-radius: 10px;
            }
            .header {
                background: #fde047;
                color: #222;
                padding: 14px;
                border-radius: 8px;
                text-align: center;
            }
            .header h1 {
                margin: 0;
                font-size: 30px;
            }
            .header h2 {
                margin: 4px 0 0 0;
                font-size: 20px;
                font-weight: normal;
                color: #333;
            }
            .header h4 {
                margin: 4px 0 0 0;
                font-size: 14px;
                font-weight: normal;
                color: #333;
                text-align: right;
            }
            .timestamp {
                font-size: 14px;
                text-align: right;
                margin: 10px 0 16px 0;
            }
            .timestamp div {
                margin: 4px 0;
            }
            .section {
                background: #0f172a;
                border: 1px solid #334155;
                border-radius: 8px;
                margin: 14px 0;
                overflow: hidden;
            }
            .section-title {
                margin: 0;
                padding: 10px 14px;
                color: #fff;
                font-weight: 800;
            }
            .sec-secret {
                background: linear-gradient(90deg,#0ea5e9,#38bdf8);
            }
            .sec-code {
                background: linear-gradient(90deg,#10b981,#34d399);
            }
            .sec-dep {
                background: linear-gradient(90deg,#8b5cf6,#a78bfa);
            }
            .card {
                padding: 14px;
            }
            .item {
                background: #111827;
                border: 1px solid #374151;
                border-radius: 8px;
                padding: 10px;
                margin: 10px 0;
            }
            .k {
                font-weight: 700;
                color: #e7650f;
                min-width: 140px;
                display: inline-block;
            }
            code {
                background: #111;
                padding: 2px 6px;
                border-radius: 4px;
            }
            .sev-critical {
                background: #fecaca;
                color: #7f1d1d;
                padding: 2px 6px;
                border-radius: 6px;
                font-weight: 700;
            }
            .sev-high {
                background: #fee2e2;
                color: #991b1b;
                padding: 2px 6px;
                border-radius: 6px;
                font-weight: 700;
            }
            .sev-medium {
                background: #fef3c7;
                color: #92400e;
                padding: 2px 6px;
                border-radius: 6px;
                font-weight: 700;
            }
            .sev-low {
                background: #d1fae5;
                color: #065f46;
                padding: 2px 6px;
                border-radius: 6px;
                font-weight: 700;
            }
            .sev-info {
                background: #e0e7ff;
                color: #3730a3;
                padding: 2px 6px;
                border-radius: 6px;
                font-weight: 700;
            }
            footer {
                margin-top: 20px;
                text-align: center;
                background: #fde047;
                color: #222;
                padding: 10px;
                border-radius: 6px;
            }
    """

    html = f"""<!DOCTYPE html>
            <html lang="en"><head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width,initial-scale=1.0">
                <title>{title} SAST Report</title>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
                <style>{css}</style>
            </head>
            <body>
            <div class="container">
                <div class="header">
                    <h1><span style="font-size: 1.5em;">🕵️</span> {title}</h1>
                    <h2>📊 {report_type} - Total Findings ({total_findings})</h2>
                    <h4>Application: {app_name} | Version: {app_version} | Technology: {app_technology}</h4>
                </div>
                <div class="timestamp">
                    <div>🕒 Report Generated: {timestamp}</div>
                </div>
            """

    # 🔹 Render each section
    def render_section(name, section_issues, icon, css_class):
        nonlocal html
        html += f'<div class="section">'
        html += f'<div class="section-title {css_class}"><span style="font-size:1.25em;">{icon}</span> {name} ({len(section_issues)})</div>'
        html += '<div class="card">'
        if not section_issues:
            html += '<div class="item">No issues found.</div>'
        for issue in section_issues:
            html += '<div class="item">'
            for k, v in issue.items():
                if isinstance(v, (dict, list)):
                    v = str(v)
                v = ihtml.escape(str(v))
                if k.lower() in ("severity", "impact"):
                    html += f'<div><span class="k">{k.capitalize()}:</span> <span class="sev-{v.lower()}">{v}</span></div>'
                else:
                    html += f'<div><span class="k">{k.capitalize()}:</span> {v}</div>'
            html += '</div>'
        html += '</div></div>'

    render_section("Secret Scanner", issues["Secret Scanner"], "🔑", "sec-secret")
    render_section("Code Analyzer", issues["Code Analyzer"], "🧑‍💻", "sec-code")
    render_section("Dependency Scan", issues["Dependency Scan"], "📚", "sec-dep")

    html += f"""
        <footer>
            {footer} &middot; © {year} {company}
        </footer>
    </div></body></html>
    """
    return html

def generate(results, config):
    report_dir = config.get('report_dir', './reports')
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, 'security_report.html')

    with open(report_path, 'w', encoding='utf-8') as f:
        html = render_html(results, config)
        f.write(html)

    print(Fore.LIGHTMAGENTA_EX + f"\n[+] HTML report generated at: {report_path}", flush=True)
