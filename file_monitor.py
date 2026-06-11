import hashlib
import os
import json
import datetime
import time

MONITOR_FILE = "file_hashes.json"

def get_hash(filepath):
    try:
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except:
        return None

def scan_folder(folder):
    hashes = {}
    for root, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)
            h = get_hash(path)
            if h:
                hashes[path] = h
    return hashes

def save_baseline(folder):
    print(f"\n[*] Creating baseline for: {folder}")
    hashes = scan_folder(folder)
    with open(MONITOR_FILE, 'w') as f:
        json.dump(hashes, f, indent=2)
    print(f"[✅] Baseline saved! {len(hashes)} files recorded")
    return hashes

def check_integrity(folder):
    print(f"\n[*] Checking integrity of: {folder}")
    if not os.path.exists(MONITOR_FILE):
        print("[❌] No baseline found! Create one first!")
        return

    with open(MONITOR_FILE, 'r') as f:
        baseline = json.load(f)

    current = scan_folder(folder)
    alerts = []

    # Modified files
    for path, old_hash in baseline.items():
        if path in current:
            if current[path] != old_hash:
                alerts.append(
                f"🚨 MODIFIED: {path}")
        else:
            alerts.append(
            f"❌ DELETED: {path}")

    # New files
    for path in current:
        if path not in baseline:
            alerts.append(
            f"⚠️  NEW FILE: {path}")

    if alerts:
        print(f"\n[!] {len(alerts)} ALERTS FOUND:")
        for a in alerts:
            print(f"    {a}")
    else:
        print("\n[✅] All files intact! No tampering detected!")

    print(f"\nFiles checked: {len(current)}")

def monitor_realtime(folder, interval=10):
    print(f"\n[*] Real-time monitoring: {folder}")
    print(f"[*] Checking every {interval} seconds")
    print("[*] Press CTRL+C to stop\n")

    if not os.path.exists(MONITOR_FILE):
        save_baseline(folder)

    scan_count = 0
    try:
        while True:
            scan_count += 1
            time_now = datetime.datetime.now(
            ).strftime('%H:%M:%S')
            print(f"[Scan #{scan_count}] {time_now}")
            check_integrity(folder)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n[*] Monitoring stopped!")

while True:
    print("\n================================")
    print("  CYBER CELL FILE MONITOR")
    print("  By Jayesh Goyal")
    print("================================")
    print("1. Create Baseline")
    print("2. Check Integrity Now")
    print("3. Real-time Monitoring")
    print("4. Exit")
    choice = input("\nChoice: ")
    if choice == '1':
        f = input("Enter folder path: ")
        save_baseline(f)
    elif choice == '2':
        f = input("Enter folder path: ")
        check_integrity(f)
    elif choice == '3':
        f = input("Enter folder path: ")
        monitor_realtime(f)
    elif choice == '4':
        break
