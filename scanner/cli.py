import argparse
import json
from scanner.shodan_parser import check_shodan
from scanner.nmap_scanner import scan_with_nmap
from scanner.utils import increment_ip
from scanner.nmap_checker import ensure_nmap_installed


def parse_args_or_prompt():
    parser = argparse.ArgumentParser(description="Scanner IPs avec Shodan et Nmap")

    parser.add_argument('--ip', type=str, help='Adresse IP de départ')
    parser.add_argument('--max-attempts', type=int, default=1,
                        help='Nombre d’IPs à scanner (par défaut: 1)')
    parser.add_argument('--nmap-scan-type', type=str, choices=['-sS', '-sT'],
                        help='Type de scan Nmap : -sS (SYN scan), -sT (TCP connect)')
    parser.add_argument('--nmap-scan-version', action='store_true',
                        help='Ajouter l’option -sV pour détecter les versions de services')
    parser.add_argument('--json-output', action='store_true',
                        help='Exporter les résultats au format JSON')
    parser.add_argument('--output-file', type=str,
                        help='Chemin du fichier de sortie JSON')

    args = parser.parse_args()

    if not args.ip:
        print("\n🔧 Aucune option fournie. Passons en mode interactif.\n")
        args.ip = input("Adresse IP de départ (ex: 192.168.1.1): ")
        args.max_attempts = int(input("Nombre d'IPs à scanner [default: 1]: ") or 1)

        print("\nQuel type de scan voulez-vous faire ?")
        print("  -sS : SYN Scan (discret, rapide, nécessite privilèges root)")
        print("  -sT : TCP Connect (plus visible, mais fonctionne sans privilèges)")
        scan_type = input("Choix du scan Nmap [-sS/-sT] (laisser vide pour ignorer) : ").strip()
        args.nmap_scan_type = scan_type if scan_type in ('-sS', '-sT') else None

        nmap_input = input("Ajouter le scan de version (-sV) ? [y/N]: ")
        args.nmap_scan_version = nmap_input.strip().lower() in ('y', 'yes')

        json_input = input("Exporter les résultats en JSON ? [y/N]: ")
        args.json_output = json_input.strip().lower() in ('y', 'yes')
        if args.json_output:
            args.output_file = input("Chemin du fichier JSON (laisser vide pour afficher): ").strip() or None

    return args


def main():
    args = parse_args_or_prompt()

    if (args.nmap_scan_type or args.nmap_scan_version) and not ensure_nmap_installed():
        print("[!] Nmap non installé, scan Nmap annulé.")
        args.nmap_scan_type = None
        args.nmap_scan_version = False

    ip = args.ip
    scan_results = []

    for i in range(args.max_attempts):
        print(f"\n[🔍] Vérification de l'IP : {ip}")
        open_ports = check_shodan(ip)

        result = {
            "ip": ip,
            "shodan_ports": open_ports or [],
        }

        if args.nmap_scan_type or args.nmap_scan_version:
            if open_ports:
                port_numbers = [int(p['port']) for p in open_ports if str(p.get('port', '')).isdigit()]
                nmap_result = scan_with_nmap(ip, port_numbers,
                                             scan_type=args.nmap_scan_type,
                                             version_scan=args.nmap_scan_version)
                result["nmap"] = nmap_result

        scan_results.append(result)
        ip = increment_ip(ip)

    if args.json_output:
        json_data = json.dumps(scan_results, indent=4)
        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(json_data)
            print(f"\n Résultats enregistrés dans {args.output_file}")
        else:
            print("\n Résultats JSON :\n")
            print(json_data)
    else:
        for res in scan_results:
            if res.get('shodan_ports'):
                print(f"\n{res['ip']}")
                print(f"\tOpen Ports")
                print(f"\t\tshodan")
                for port_info in res['shodan_ports']:
                    print(f"\t\t\tPort {port_info['port']}")
                    if 'service' in port_info and port_info['service']:
                        print(f"\t\t\t\tService: {port_info['service']}")
                if 'nmap' in res:
                    print(f"\t\tnmap")
                    lines = res['nmap'].splitlines()
                    for line in lines:
                        if '/tcp' in line or '/udp' in line:
                            parts = line.split()
                            if len(parts) >= 3:
                                port_proto = parts[0]
                                state = parts[1]
                                service = parts[2]
                                version = " ".join(parts[3:]) if len(parts) > 3 else None

                                print(f"\t\t\tPort {port_proto}")
                                print(f"\t\t\t\tÉtat: {state}")
                                print(f"\t\t\t\tService: {service}")
                                if version:
                                    print(f"\t\t\t\tVersion: {version}")
            else:
                print(f"[✘] Aucun résultat ou pas de ports trouvés pour {res['ip']}")


if __name__ == "__main__":
    main()
