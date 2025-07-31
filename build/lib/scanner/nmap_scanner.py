

import shutil
import subprocess

def is_nmap_installed():
    """Vérifie si Nmap est disponible dans le PATH."""
    return shutil.which("nmap") is not None



def scan_with_nmap(ip, ports=None):
    port_str = ",".join(str(p) for p in ports) if ports else ""
    command = ["nmap", "-sV", "-Pn", ip]
    if port_str:
        command += ["-p", port_str]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=60)
        return result.stdout
    except Exception as e:
        return f"[Nmap error] {e}"
