import time
import random
from scanner.shodan_parser import check_shodan
from scanner.nmap_scanner import scan_with_nmap,is_nmap_installed
from scanner.utils import increment_ip,suggest_nmap_install

def main():
    if not is_nmap_installed():
        suggest_nmap_install()
        choix = input("\nVoulez-vous continuer SANS Nmap ? (o/n) : ").lower()
        if choix != "o":
            print("Arrêt du programme.")
            return
    #ips = ["216.234.210.137","216.234.210.138","216.234.210.232","216.234.210.245","216.234.210.246","216.234.210.247","216.234.210.248","216.234.210.249","216.234.210.251","216.234.211.51"]
    ip = "98.97.151.85"
    count = 0
    max_attempts = 2# Sécurité : nombre max d’IP à scanner

    while count < max_attempts:
        print(f"[+] Vérification de l'IP : {ip}")
        open_ports = check_shodan(ip)

        if open_ports:
            print(f"\n{ip}")
            print(f"\tOpen Ports ")
            print(f"\t\t shodan")
            for port_info in open_ports:
                print(f"\t\t\tPort {port_info['port']}")
                if port_info['service']:
                    print(f"\t\t\t\tService: {port_info['service']}")
            if is_nmap_installed():
                port_numbers = [int(p['port']) for p in open_ports if p['port'].isdigit()]
                print(f"\n  Nmap Scan :")
                nmap_result = scan_with_nmap(ip, port_numbers)
                print(nmap_result)
        else:
            print(f"[✘] Aucun résultat ou pas de ports trouvés pour {ip}")

        delay = random.uniform(5, 15)
        print(f"[~] Pause de {delay:.1f} secondes...\n")
        time.sleep(delay)

        ip = increment_ip(ip)
        count += 1


if __name__ == "__main__":
    main()
