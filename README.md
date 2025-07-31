# Shodan-Scan

**Shodan-Scan** is a command-line tool designed to simplify the collection, scanning, and presentation of results from Shodan and Nmap.

---

## What is it for?

This tool allows you to:

- **Scan IP address ranges** via Shodan to quickly identify open ports and associated services.
- **Perform optional Nmap scans** (e.g., `-sV` or other user-chosen types) on discovered ports to enrich information (service versions, port states, etc.).
- **Present results clearly and structured**, compatible with mind-mapping tools like ***XMind***, accelerating scan analysis and visualization.

---

## Important Notes

- For better coverage and to reduce the risk of request blocking, it is recommended to **use a VPN periodically** while scanning.
- The results are **not 100% reliable** due to dynamic network conditions, possible blocking, or incomplete Shodan data.
- This tool acts as a **basic alternative to Shodan’s paid API**, offering limited but useful scan capabilities without requiring a subscription.

---

## Features

- Automatic incrementation of IP addresses for range scanning.
- Detection of open ports and services via Shodan.
- Configurable Nmap scanning with different scan types.
- JSON export of results for further processing or integration.
- Interactive and CLI argument modes.
- Automatic detection of Nmap installation with optional installation prompt.
- Compatible with Windows, Linux, and macOS.

---

##  Installation

###  Requirements

- Python 3.8+
- `nmap` must be installed on your system (Linux/Kali: usually pre-installed, Windows: install manually)

###  Install Nmap

- **Linux (Debian/Ubuntu/Kali)**  
  ```bash
  sudo apt update
  sudo apt install nmap


* **Windows**
  Download and install from: [https://nmap.org/download.html](https://nmap.org/download.html)
  Ensure `nmap` is added to your system PATH.

---

###  Install this tool via GitHub

1. Clone the repo:

```bash
git clone https://github.com/Medmas07/shodan_scanner.git
cd shodan-nmap-scanner
```

2. Install as a CLI tool:

```bash
pip install .
```

3. Now you can run:

```bash
shodan-scan --ip 192.168.1.1 --max-attempts 3 --nmap-scan-version
```

---
##  Download

You can download the latest `.exe` build for Windows here:

👉 [Download shodan-scan.exe (latest)](https://github.com/Medmas07/shodan_scanner/releases/download/v1.0.0/shodan-scan.exe)

⚠️ Make sure to have `nmap` installed and available in your PATH.

##  Usage

```bash
shodan-scan [OPTIONS]
```

### Common Options
| Option                   | Description                                                            |
| ------------------------ | ---------------------------------------------------------------------- |
| `--ip`                   | Starting IP address to scan                                            |
| `--max-attempts`         | Number of consecutive IPs to scan (default: 1)                         |
| `--nmap-scan-version`    | Enable Nmap service version detection                                  |
| `--nmap-scan-type`       | Choose scan type: `-sS` (stealth SYN scan) or `-sT` (TCP connect scan) |
| `--json-output`          | Export result in JSON format                                           |
| `--output-file filename` | Save JSON output to file                                               |


### Example:

```bash
shodan-scan --ip 192.168.1.1 --max-attempts 3 --nmap-scan-version --json-output --output-file result.json
```

---

## 📂 Output Example

### Shodan + Nmap text output:

```
192.168.1.1
    Open Ports
        shodan
            Port 80
                Service: http
            Port 443
                Service: https
        nmap
            Port 80
                Service: Apache httpd
                Version: 2.4.41
```
