from pathlib import Path
from datetime import datetime
import json


def generate_html_report(results, output_dir="Reports/output"):
    """
    Generate a consolidated HTML report from scan results.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_path = output_dir / "security_report.html"

    style = """
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f9f9f9; }
        h1 { color: #2c3e50; }
        h2 { color: #34495e; background: #ecf0f1; padding: 6px; border-radius: 6px; }
        .issue { border: 1px solid #ddd; padding: 10px; margin-bottom: 6px; border-radius: 6px; background: #fff; }
        .severity-High { border-left: 6px solid #e74c3c; }
        .severity-Medium { border-left: 6px solid #f39c12; }
        .severity-Low { border-left: 6px solid #27ae60; }
        .no-issues { color: green; font-weight: bold; }
    </style>
    """

    html = [f"<html><head>{style}</head><body>"]
    html.append(f"<h1>🔐 Security Report</h1>")
    html.append(f"<p><b>Generated:</b> {timestamp}</p>")

    for tool, findings in results.items():
        html.append(f"<h2>{tool} Results ({len(findings)})</h2>")
        if not findings:
            html.append("<p class='no-issues'>✅ No issues found.</p>")
        else:
            for issue in findings:
                sev = issue.get("severity", "Unknown")
                msg = issue.get("message", str(issue))
                html.append(f"<div class='issue severity-{sev}'>")
                html.append(f"<b>Severity:</b> {sev}<br>")
                html.append(f"<b>Details:</b> {msg}")
                html.append("</div>")

    html.append("</body></html>")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html))

    return html_path


def generate_json_report(results, output_dir="Reports/output"):
    """
    Generate a consolidated JSON report from scan results.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "security_report.json"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    return json_path
