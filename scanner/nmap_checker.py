import subprocess
import sys
import platform

def is_nmap_installed():
    try:
        subprocess.run(["nmap", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_nmap_linux():
    # Tu peux étendre selon la distro (apt, yum, pacman, etc.)
    print("Tentative d'installation de nmap via apt (Linux)...")
    subprocess.run(["sudo", "apt-get", "update"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "nmap"])

def install_nmap_windows():
    print("Merci d’installer Nmap manuellement depuis https://nmap.org/download.html#windows")

def ensure_nmap_installed():
    if is_nmap_installed():
        return True

    print("[!] Nmap n'est pas installé.")
    choice = input("Voulez-vous essayer de l'installer maintenant ? [y/N]: ").strip().lower()

    if choice not in ('y', 'yes'):
        return False

    system = platform.system()
    if system == "Linux":
        install_nmap_linux()
    elif system == "Windows":
        install_nmap_windows()
    else:
        print(f"Installation automatique non supportée pour {system}. Veuillez installer Nmap manuellement.")
        return False

    # Vérifie à nouveau après installation
    if is_nmap_installed():
        print("[✓] Nmap est maintenant installé.")
        return True
    else:
        print("[✗] Échec de l'installation automatique de Nmap.")
        return False
