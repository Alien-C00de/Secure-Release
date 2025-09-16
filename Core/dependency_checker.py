import os
import json
import asyncio
import tempfile
from pathlib import Path
from colorama import Fore, Style
from Utils import config
cfg = config.load_config("config.yaml")
from Core.logger import setup_logger
logger = setup_logger("dep-checker", cfg)


async def scan(config):
    print(Fore.CYAN + f"[+] 📦 Running Dependency Scan...", flush=True)
    results = []

    # Check which languages are defined in the config
    dependency_files = config.get('dependency_files', {})

    if 'python' in dependency_files:
        results += await scan_python(config, dependency_files['python'])
    if 'node' in dependency_files:
        results += await scan_node(config, dependency_files['node'])
    if 'java' in dependency_files:
        results += await scan_java(config)
    if 'dotnet' in dependency_files:
        results += await scan_dotnet(config, dependency_files['dotnet'])

    # print(f"[+] Dependency scan complete: {len(results)} issues found.")
    print(Fore.CYAN + Style.BRIGHT + f"[+] 📢 Dependency scan found" + Fore.WHITE + Style.BRIGHT, len(results), Fore.CYAN + Style.BRIGHT + f"issues.\n", Fore.RESET)
    return results


# Async subprocess runner that streams output to the terminal
async def run_subprocess_old(command):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT
    )

    output_lines = []
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        decoded_line = line.decode().rstrip()
        print(decoded_line)  # Real-time terminal output
        output_lines.append(decoded_line)

    await process.wait()

    if process.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {process.returncode}")

    return "\n".join(output_lines)

async def scan_python(config, python_files):
    print("[>] Scanning Python dependencies with Safety (scan)...")
    results = []

    for dep_file in python_files:
        files = find_files(config, dep_file)
        for req_file in files:
            try:
                print(f"[>] Running: safety scan --json --file={req_file}")
                output = await run_subprocess(f"safety scan --output json --file={req_file}")
                print(f"[+] Safety scan report for {req_file} generated successfully.")

                # Trim leading non-JSON content, if any
                json_start = output.find("{")
                if json_start == -1:
                    raise ValueError("No JSON object found in output.")
                clean_output = output[json_start:]
                parsed = json.loads(clean_output)

                projects = parsed.get("scan_results", {}).get("projects", [])
                for project in projects:
                    for file_entry in project.get("files", []):
                        file_path = file_entry.get("location", "unknown")

                        for dependency in file_entry.get("results", {}).get("dependencies", []):
                            package_name = dependency.get("name", "unknown")

                            for spec in dependency.get("specifications", []):
                                vulns = spec.get("vulnerabilities", {}).get("known_vulnerabilities", [])
                                for vuln in vulns:
                                    ignored_reason = (vuln.get("ignored") or {}).get("reason") or ""
                                    if "See " in ignored_reason:
                                        more_info_url = ignored_reason.split("See ")[-1].strip()
                                    else:
                                        more_info_url = "N/A"
                                    results.append({
                                        "file": file_path,
                                        "package": package_name,
                                        "version": spec.get("version") or "unknown",
                                        "vuln_id": vuln.get("id") or "N/A",
                                        "severity": ((vuln.get("ignored") or {}).get("code") or "unknown").upper(),
                                        "vulnerable_spec": vuln.get("vulnerable_spec") or "unknown",
                                        "description": ((vuln.get("ignored") or {}).get("reason") or "")[:150],
                                        "fixed_versions": [],  # Still not available directly
                                        "ignored_reason": ignored_reason,
                                        "more_info_url": more_info_url
                                    })

            except Exception as e:
                print(f"[!] Safety scan failed for {req_file}: {e}")
                logger.warning(f"Safety scan failed for {req_file}")
                logger.error(f"Error during scan: {e}")

    return results

# Node.js: npm audit
async def scan_node(config, node_files):
    print("[>] Scanning Node.js dependencies...")
    results = []
    for dep_file in node_files:
        files = find_files(config, dep_file)
        for file in files:
            dir_path = os.path.dirname(file)
            try:
                output = await run_subprocess(f"npm audit --json", cwd=dir_path)
                audit_data = json.loads(output)
                advisories = audit_data.get("vulnerabilities", {})
                for pkg, info in advisories.items():
                    results.append({
                        "file": file,
                        "package": pkg,
                        "version": info.get("installedVersion"),
                        "vuln_id": info.get("via", [{}])[0].get("source", "N/A"),
                        "severity": info.get("severity"),
                        "description": info.get("via", [{}])[0].get("title", "")[:150]
                    })
            except Exception as e:
                print(f"[!] Node audit failed: {e}")
    return results

async def run_subprocess(cmd):
    # print(f"[>] Running command: {cmd}")
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        shell=True  # Needed to run .bat files on Windows
    )
    stdout, stderr = await process.communicate()

    # if stdout:
    #     print(stdout.decode())
    # if stderr:
    #     print(stderr.decode())

    if process.returncode != 0:
        raise Exception(f"Command failed with exit code {process.returncode}")
    
async def scan_java(config):
    # print("[>] Scanning Java dependencies...")
    results = []

    dirs = config.get('target_dirs', ['.'])
    if isinstance(dirs, list) and len(dirs) == 1 and isinstance(dirs[0], list):
        dirs = dirs[0]

    dep_check_path = config.get('tools', {}).get('dependency_check', 'dependency-check.bat')
    dep_check_path_quoted = f'"{Path(dep_check_path)}"'

    for d in dirs:
        try:
            if isinstance(d, list):
                d = d[0]
            scan_dir_quoted = f'"{Path(d).resolve()}"'

            report_path = os.path.join(tempfile.gettempdir(), "depcheck-report.json")
            report_path_quoted = f'"{report_path}"'

            project_name = "ProjScan"
            cmd = f'{dep_check_path_quoted} --project "{project_name}" --scan {scan_dir_quoted} --format JSON --out {report_path_quoted} --noupdate'
            # print(f"[>] Running command:\n{cmd}")
            await run_subprocess(cmd)

            # Parse JSON report
            with open(report_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                dependencies = data.get("dependencies", [])

                for dep in dependencies:
                    file_name = dep.get("fileName", "unknown")
                    file_path = dep.get("filePath", "unknown")
                    
                    for vuln in dep.get("vulnerabilities", []):
                        results.append({
                            "fileName": file_name,
                            "filePath": file_path,
                            "name": vuln.get("name", "N/A"),  # CVE ID
                            "severity": vuln.get("severity", "unknown"),
                            "description": (vuln.get("description") or "")[:150]
                        })
                        # print(f"[+] Found vulnerability: {vuln.get('name')} in {file_name}")

        except Exception as e:
            print(f"[!] Java audit failed: {e}")

    return results

# .NET: dotnet list package
async def scan_dotnet(config, dotnet_files):
    print("[>] Scanning .NET dependencies...")
    results = []
    for dep_file in dotnet_files:
        files = find_files(config, dep_file)
        for file in files:
            dir_path = os.path.dirname(file)
            try:
                output = await run_subprocess("dotnet list package --vulnerable --include-transitive", cwd=dir_path)
                for line in output.splitlines():
                    if "[" in line and "]" in line:
                        parts = line.strip().split()
                        if len(parts) >= 3:
                            results.append({
                                "file": file,
                                "package": parts[0],
                                "version": parts[1],
                                "vuln_id": parts[-1].strip('[]'),
                                "severity": "Unknown",
                                "description": "Vulnerability found via .NET audit"
                            })
            except Exception as e:
                print(f"[!] .NET audit failed: {e}")
    return results

# Utility to find files
def find_files(config, filename):
    targets = config.get('target_dirs', ['.'])
    matches = []
    for path in targets:
        for root, _, files in os.walk(path):
            for f in files:
                if f == filename:
                    matches.append(os.path.join(root, f))
    return matches