import asyncio
import json
import os
from pathlib import Path
import tempfile
from colorama import Fore, Style

def is_bandit_available():
    try:
        import bandit
        return True
    except ImportError:
        return False

async def scan(config):
    # print("\n[+] Running Static Code Analyzer (Bandit)...")
    print(Fore.LIGHTGREEN_EX + f"\n[+] 🧑‍💻 Running Static Code Analyzer (Bandit)...", flush=True)
    results = []

    if not is_bandit_available():
        print("[!] Bandit is not installed. Skipping code analysis.")
        return results

    target_dirs = config.get("target_dirs", ["."])
    if isinstance(target_dirs, list) and len(target_dirs) == 1 and isinstance(target_dirs[0], list):
        target_dirs = target_dirs[0]

    for directory in target_dirs:
        directory = Path(directory).resolve()
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".json") as tmp_report:
            cmd = f'bandit -r "{directory}" -f json -o "{tmp_report.name}"'
            # print(cmd)

            tmp_path = tmp_report.name
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            # Ensure Bandit has finished writing
            await asyncio.sleep(0.1)  # Give OS time to flush
            try:
                with open(tmp_path, 'r') as f:
                    bandit_result = json.load(f)
                    # print(f"[+] Bandit report for {directory} generated successfully.")
                    for issue in bandit_result.get("results", []):
                        # print(f"[+] Found issue: {issue.get('test_name')} in {issue.get('filename')} at line {issue.get('line_number')}")
                        results.append({
                            "impact": issue.get("issue_severity"),
                            "file": issue.get("filename"),
                            "line": issue.get("line_number"),
                            "pattern name": issue.get("test_name"),
                            "line_content": issue.get("issue_text")
                        })
            except Exception as e:
                print(f"[!] Failed to parse Bandit report: {e}")

            try:
                os.remove(tmp_path)
            except Exception as e:
                print(f"[!] Could not delete temp file: {e}")

    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + f"[+] 📢 Static Code Analyzer found" + Fore.WHITE + Style.BRIGHT, len(results), Fore.LIGHTGREEN_EX + Style.BRIGHT + f"issues.", Fore.RESET)
    return results