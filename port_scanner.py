import socket
import datetime

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            return True
        return False
    except:
        return False

def get_service(port):
    services = {
        21: "FTP",
        22: "SSH",
        23: "Telnet (DANGEROUS!)",
        25: "SMTP Email",
        53: "DNS",
        80: "HTTP Web",
        110: "POP3 Email",
        143: "IMAP Email",
        443: "HTTPS Secure Web",
        445: "SMB (WannaCry used this!)",
        3306: "MySQL Database",
        3389: "Remote Desktop",
        8080: "HTTP Alternate"
    }
    return services.get(port, "Unknown Service")

print("=" * 40)
print("   CYBER CELL PORT SCANNER")
print("   By Jayesh Goyal")
print("=" * 40)

target = input("\nEnter IP to scan: ")
print(f"\nScanning {target}...")
print(f"Time: {datetime.datetime.now()}")
print("-" * 40)

open_ports = []

common_ports = [21,22,23,25,53,80,110,143,443,445,3306,3389,8080]

for port in common_ports:
    print(f"Checking port {port}...", end="\r")
    if scan_port(target, port):
        service = get_service(port)
        open_ports.append(port)
        print(f"[OPEN]  Port {port} → {service}    ")

print("-" * 40)
if open_ports:
    print(f"Found {len(open_ports)} open ports!")
else:
    print("No open ports found!")
print("Scan complete!")
print("=" * 40)
