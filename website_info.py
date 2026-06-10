import subprocess
import socket
import datetime

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True,
        capture_output=True, text=True, timeout=10)
        return result.stdout
    except:
        return "Could not fetch"

def get_website_info(domain):
    print("\n" + "="*45)
    print("   CYBER CELL WEBSITE ANALYZER")
    print("   By Jayesh Goyal")
    print("="*45)
    print(f"Target: {domain}")
    print(f"Time: {datetime.datetime.now()}")
    print("="*45)

    # IP Address
    print("\n[1] IP ADDRESS:")
    try:
        ip = socket.gethostbyname(domain)
        print(f"    {domain} → {ip}")
    except:
        print("    Could not resolve IP")
        ip = None

    # WHOIS
    print("\n[2] WHOIS INFO (Owner Details):")
    whois = run_cmd(f"whois {domain}")
    important = ['Registrar:', 'Creation Date:',
    'Expiry Date:', 'Country:', 'Registrant:',
    'Name Server:']
    for line in whois.split('\n'):
        for key in important:
            if key.lower() in line.lower():
                print(f"    {line.strip()}")
                break

    # DNS Records
    print("\n[3] DNS RECORDS:")
    dns = run_cmd(f"nslookup {domain}")
    print(f"    {dns[:200]}")

    # Nmap scan
    if ip:
        print("\n[4] OPEN PORTS (Nmap scan):")
        ports = run_cmd(f"nmap -F {ip}")
        for line in ports.split('\n'):
            if 'open' in line:
                print(f"    ✓ {line.strip()}")

    print("\n" + "="*45)
    print("SCAN COMPLETE!")
    print("="*45 + "\n")

while True:
    domain = input("Enter website (e.g. google.com)"
    " or 'quit': ")
    if domain == 'quit':
        break
    get_website_info(domain)
