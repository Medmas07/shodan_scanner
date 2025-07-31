import requests
from bs4 import BeautifulSoup
import random
from .utils import USER_AGENTS

def check_shodan(ip):
    headers = {
        "User-Agent": random.choice(USER_AGENTS)
    }

    url = f"https://www.shodan.io/search?query={ip}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse le contenu HTML pour extraire les ports
        soup = BeautifulSoup(response.text, 'html.parser')
        ports_div = soup.find("div", {"id": "ports"})
        if ports_div:
            ports = []
            for a in ports_div.find_all("a"):
                port = a.text.strip()

                # Extraction du nom du service (si existant)
                port_details = extract_service_name(soup, port)
                ports.append({
                    'port': port,
                    'service': port_details if port_details else None
                })
            return ports
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"[!] Erreur pour {ip} : {e}")
        return None


def extract_service_name(soup, port):
    # Trouver l'en-tête du port, ex: <h6 id="443" class="grid-heading">
    port_header = soup.find("h6", {"id": port})
    if not port_header:
        return None

    # [1] Cas Web : chercher un titre HTTP (présent pour les services web comme HTTP, HTTPS)
    http_title = port_header.find_next("div", {"class": "http-title"})
    if http_title:
        title_text = http_title.get_text(strip=True)
        if title_text:
            return title_text

    # [2] Cas non-Web : chercher les bannières de service (SSH, FTP, etc.)
    card = port_header.find_next("div", {"class": "card card-padding banner"})
    if card:
        link = card.find("a")
        if link and link.text.strip():
            return link.text.strip()

    # Si rien trouvé
    return None

