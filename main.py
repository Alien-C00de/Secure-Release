import argparse
import asyncio
import os
import pyfiglet
from time import perf_counter
from colorama import Fore, Style
from Core import (
    code_analyzer_py,
    secret_scanner,
    dependency_checker,
    # policy_validator,
    # image_checker,
    code_analyzer,
)
from Reports import html_report, json_report, notifier
from Utils import config

async def run_scans(cfg: dict):
    """Run all enabled scans and collect results."""
    print("[+] Code Scanning Started...")
    start_time = perf_counter()

    # Launch scans concurrently (each function takes cfg explicitly)
    results = await asyncio.gather(
        dependency_checker.scan(cfg),
        secret_scanner.scan(cfg),
        code_analyzer.scan(cfg),
        # policy_validator.scan(cfg),
        # image_checker.scan(cfg)
    )

    combined_results = {
        "Dependency Scan": results[0],
        "Secret Scanner": results[1],
        "Code Analyzer": results[2],
        # "policies": results[3],
        # "containers": results[4],
    }

    # Generate reports
    html_report.generate(combined_results, cfg)
    json_report.generate(combined_results, cfg)

    # Trigger alerts if configured
    notifier.send_alerts(combined_results, cfg)

    print(Fore.LIGHTBLUE_EX + f"[+] Security scans completed. Reports generated.")
    print(
        Fore.YELLOW
        + Style.BRIGHT
        + f"\n⏱️ Total Time Taken: {round(perf_counter() - start_time, 2)} Seconds.",
        flush=True,
    )
    print(Style.RESET_ALL)


def main():
    # Clear terminal screen
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

    # CLI args
    parser = argparse.ArgumentParser(description="CI/CD Pipeline Security Tool")
    parser.add_argument(
        "-c", "--config", required=True, help="Path to configuration YAML file"
    )
    args = parser.parse_args()

    # Load config once
    cfg = config.load_config(args.config)

    # Fancy header
    figlet_name = cfg.get("tool_info", {}).get("tool_name", "Tool Name")
    terminal_header = pyfiglet.figlet_format(figlet_name, font="doom")
    print(Fore.YELLOW + Style.BRIGHT + terminal_header + Fore.RESET + Style.RESET_ALL)

    # Pass cfg everywhere (no globals)
    footer_owner = cfg.get("tool_info", {}).get("owner_title", "Footer Owner")
    author = cfg.get("tool_info", {}).get("author", "Author")
    year = cfg.get("tool_info", {}).get("year", "2025")
    email = cfg.get("tool_info", {}).get("email", "email@example.com")
    github = cfg.get("tool_info", {}).get("github", "https://github.com/your-repo")
    version = cfg.get("tool_info", {}).get("version", "1.0.0")

    asyncio.run(run_scans(cfg))
    print(Fore.YELLOW + f"📢 {footer_owner} 👽: {author} Ver: {version} © {year}", flush=True)
    print(Fore.YELLOW + f"📥 {email} ", flush=True)
    print(Fore.YELLOW + f"🚀 {github}", flush=True)
    print(Style.RESET_ALL)

if __name__ == "__main__":
    main()
