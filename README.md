# Shodan-Scan

**Shodan-Scan** is a command-line tool designed to simplify the collection, scanning, and presentation of results from Shodan and Nmap.

---

## What is it for?

This tool allows you to:

- **Scan IP address ranges** via Shodan to quickly identify open ports and associated services.
- **Perform optional Nmap scans** (e.g., `-sV` or other user-chosen types) on discovered ports to enrich information (service versions, port states, etc.).
- **Present results clearly and structured**, compatible with mind-mapping tools like **XMind**, accelerating scan analysis and visualization.

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

## Installation

```bash
pip install shodan-scan
