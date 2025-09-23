import smtplib
from email.mime.text import MIMEText
import json
import requests

def send_alerts(results, config):
    if config.get("notify", {}).get("email"):
        send_email_alert(results, config)
    if config.get("notify", {}).get("slack"):
        send_slack_alert(results, config)


def send_email_alert(results, config):
    try:
        smtp_cfg = config.get("smtp", {})
        to_email = smtp_cfg.get("to")
        from_email = smtp_cfg.get("from")
        smtp_server = smtp_cfg.get("server")
        smtp_port = smtp_cfg.get("port", 587)
        password = smtp_cfg.get("password")

        summary = summarize_issues(results)
        msg = MIMEText(summary)
        msg['Subject'] = 'CI/CD Security Report Alert'
        msg['From'] = from_email
        msg['To'] = to_email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, [to_email], msg.as_string())
        print("[+] Email alert sent.")
    except Exception as e:
        print(f"[!] Failed to send email alert: {e}")


def send_slack_alert(results, config):
    try:
        webhook_url = config.get("slack", {}).get("webhook_url")
        summary = summarize_issues(results)
        payload = {
            "text": f"🚨 CI/CD Security Report Summary:\n{summary}"
        }
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            print("[+] Slack alert sent.")
        else:
            print(f"[!] Slack alert failed: {response.status_code} {response.text}")
    except Exception as e:
        print(f"[!] Failed to send Slack alert: {e}")


def summarize_issues(results):
    summary = []
    for key, issues in results.items():
        summary.append(f"{key.capitalize()}: {len(issues)} issues")
    return '\n'.join(summary)
