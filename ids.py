import socket
import threading
import datetime
import time
import subprocess

def get_network():
    print("🔍 Auto-detecting your network...")
    try:
        result = subprocess.run(
        ['ip', 'addr'],
        capture_output=True, text=True)
        lines = result.stdout
        # Check hotspot
        if '192.168.43' in lines:
            print("📱 Hotspot network detected!")
            return '192.168.43'
        # Check home WiFi
        elif '192.168.1' in lines:
            print("🏠 WiFi network detected!")
            return '192.168.1'
        elif '192.168.0' in lines:
            print("🏠 WiFi network detected!")
            return '192.168.0'
        else:
            # Auto detect any network
            s = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            network = ".".join(ip.split(".")[:3])
            print(f"🌐 Network detected: {network}")
            return network
    except:
        print("⚠️  Using default hotspot network")
        return '192.168.43'

def get_my_ip():
    try:
        s = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Unknown"

PORTS_TO_CHECK = [21,22,23,80,443,3306,8080,4444]
PORT_NAMES = {
    21:"FTP",22:"SSH",23:"Telnet⚠️",
    80:"HTTP",443:"HTTPS",
    3306:"MySQL",8080:"HTTP-Alt",
    4444:"Metasploit🚨"
}
known_devices = {}
alert_log = []

def log_alert(msg):
    timestamp = datetime.datetime.now().strftime(
    "%H:%M:%S")
    alert = f"[{timestamp}] {msg}"
    alert_log.append(alert)
    print(alert)

def check_ports(ip):
    open_ports = []
    for port in PORTS_TO_CHECK:
        try:
            s = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((ip, port)) == 0:
                name = PORT_NAMES.get(port, "Unknown")
                open_ports.append(f"{port}({name})")
                if port in [23, 4444]:
                    log_alert(
                    f"🚨 DANGEROUS PORT OPEN!"
                    f" IP:{ip} Port:{port} {name}")
            s.close()
        except:
            pass
    return open_ports

def ping_ip(ip):
    try:
        s = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM)
        s.settimeout(0.3)
        s.connect_ex((ip, 80))
        s.close()
        return True
    except:
        try:
            socket.gethostbyaddr(ip)
            return True
        except:
            return False

def scan_network(network):
    active = []
    lock = threading.Lock()

    def check(ip):
        if ping_ip(ip):
            with lock:
                active.append(ip)

    threads = []
    for i in range(1, 255):
        ip = f"{network}.{i}"
        t = threading.Thread(
        target=check, args=(ip,))
        threads.append(t)
        t.start()
        if len(threads) >= 50:
            for t in threads:
                t.join()
            threads = []
    for t in threads:
        t.join()
    return active

def monitor():
    print("\n" + "="*45)
    print("  CYBER CELL IDS — BY JAYESH GOYAL")
    print("  Works on WiFi + Hotspot + Internet")
    print("="*45)

    my_ip = get_my_ip()
    print(f"Your IP: {my_ip}")

    NETWORK = get_network()
    print(f"Scanning: {NETWORK}.0/24")
    print("Press CTRL+C to stop\n")

    # Initial scan
    print("[*] Initial scan running...")
    initial = scan_network(NETWORK)
    for ip in initial:
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except:
            hostname = "Unknown"
        known_devices[ip] = hostname
        if ip != my_ip:
            ports = check_ports(ip)
            port_str = (", ".join(ports)
            if ports else "none")
            print(f"    Found: {ip}"
            f" ({hostname})"
            f" Ports: {port_str}")
        else:
            print(f"    Found: {ip} (YOUR DEVICE)")

    print(f"\n[*] {len(known_devices)}"
    f" devices found initially")
    print("[*] Monitoring started...\n")

    scan_count = 0
    try:
        while True:
            scan_count += 1
            time_now = datetime.datetime.now(
            ).strftime('%H:%M:%S')
            print(f"\n━━━ Scan #{scan_count}"
            f" at {time_now} ━━━")

            # Re-detect network (handles switching)
            current_network = get_network()
            current = scan_network(current_network)

            # New devices
            for ip in current:
                if ip not in known_devices:
                    try:
                        hostname = (
                        socket.gethostbyaddr(ip)[0])
                    except:
                        hostname = "Unknown"
                    log_alert(
                    f"🚨 NEW DEVICE JOINED!"
                    f" IP:{ip} Name:{hostname}")
                    known_devices[ip] = hostname
                    ports = check_ports(ip)
                    if ports:
                        log_alert(
                        f"⚠️  Open ports on {ip}:"
                        f" {', '.join(ports)}")

            # Disconnected devices
            for ip in list(known_devices.keys()):
                if ip not in current:
                    log_alert(
                    f"📴 Device left: {ip}"
                    f" ({known_devices[ip]})")
                    del known_devices[ip]

            print(f"Active devices: {len(current)}")
            print(f"Total alerts: {len(alert_log)}")
            print("Next scan in 30 seconds...")
            time.sleep(30)

    except KeyboardInterrupt:
        print("\n\n" + "="*45)
        print("IDS STOPPED BY USER")
        print(f"Total scans run: {scan_count}")
        print(f"Total alerts: {len(alert_log)}")
        if alert_log:
            print("\n📋 FULL ALERT LOG:")
            for a in alert_log:
                print(f"  {a}")
        print("="*45)

monitor()
