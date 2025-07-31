import subprocess
import platform
import re


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0 Safari/537.36",
]

def increment_ip(ip):
    if not ip:
        raise ValueError("IP address is missing.")
    ip_parts = list(map(int, ip.split('.')))
    ip_parts[3] += 1
    if ip_parts[3] > 255:
        ip_parts[3] = 0
        ip_parts[2] += 1
    return '.'.join(map(str, ip_parts))



def suggest_nmap_install():
    system = platform.system()

    print("[!] Nmap n’est pas installé.")
    print("    Il est nécessaire pour scanner les ports localement.")

    if system == "Windows":
        print("→ Téléchargement manuel : https://nmap.org/download.html#windows ou https://nmap.org/dist/nmap-7.97-setup.exe")
    elif system == "Linux":
        distro = get_linux_distribution()
        if distro in ["ubuntu", "debian"]:
            print("→ Commande suggérée : sudo apt install nmap")
        elif distro in ["arch", "manjaro"]:
            print("→ Commande suggérée : sudo pacman -S nmap")
        else:
            print("→ Commande suggérée : sudo yum install nmap (ou équivalent)")
    elif system == "Darwin":  # macOS
        print("→ Commande suggérée : brew install nmap")
    else:
        print("→ Veuillez installer Nmap manuellement depuis : https://nmap.org/download.html")

def get_linux_distribution():
    try:
        output = subprocess.check_output(["cat", "/etc/os-release"], text=True)
        for line in output.splitlines():
            if line.startswith("ID="):
                return line.split("=")[1].replace('"', '').lower()
    except Exception:
        return ""

def parse_nmap_output(nmap_output: str) -> list:
    ports = []
    for line in nmap_output.splitlines():
        if re.match(r'^\d+/tcp', line):
            parts = re.split(r'\s+', line.strip(), maxsplit=4)
            port = int(parts[0].split('/')[0])
            state = parts[1]
            service = parts[2]
            version = parts[3] if len(parts) > 3 else ""
            ports.append({
                "port": port,
                "state": state,
                "service": service,
                "version": version
            })
    return ports
