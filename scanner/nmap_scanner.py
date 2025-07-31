

import shutil
import subprocess
import re


def is_nmap_installed():
    """Vérifie si Nmap est disponible dans le PATH."""
    return shutil.which("nmap") is not None


def scan_with_nmap(ip, ports=None, scan_type="-sS", version_scan=True):
    port_str = ",".join(str(p) for p in ports) if ports else ""
    command = ["nmap", "-Pn", scan_type or "-sS", ip]

    if version_scan:
        command.insert(1, "-sV")  # Ajoute -sV après -Pn

    if port_str:
        command += ["-p", port_str]

    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=60)
        return result.stdout
    except Exception as e:
        return f"[Nmap error] {e}"


def parse_nmap_output(output):
    """
    Parse la sortie brute de Nmap et retourne une liste de dictionnaires.
    """
    results = []
    lines = output.splitlines()
    for line in lines:
        if re.match(r"^\d+/tcp", line.strip()):
            parts = re.split(r'\s+', line.strip(), maxsplit=4)
            if len(parts) >= 3:
                port = int(parts[0].split('/')[0])
                state = parts[1]
                service = parts[2]
                version = parts[3] if len(parts) > 3 else ""
                results.append({
                    "port": port,
                    "state": state,
                    "service": service,
                    "version": version
                })
    return results
