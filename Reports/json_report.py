import os
import json
from colorama import Fore, Style

def generate(results, config):
    report_dir = config.get('report_dir', './reports')
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, 'security_report.json')

    try:
        with open(report_path, 'w') as f:
            json.dump(results, f, indent=4)
        print(Fore.LIGHTMAGENTA_EX + f"[+] JSON report generated at: {report_path}", flush=True)
        # print(f"[+] JSON report generated at: {report_path}")
    except Exception as e:
        print(f"[!] Failed to write JSON report: {e}")
