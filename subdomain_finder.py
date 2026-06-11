import socket
import threading

def find_subdomains(domain):
    print(f"\n=== SUBDOMAIN FINDER ===")
    print(f"Target: {domain}")
    print("Scanning...\n")

    subdomains = [
        'www','mail','ftp','admin','blog',
        'shop','api','dev','test','staging',
        'portal','vpn','remote','smtp','pop',
        'imap','ns1','ns2','mx','cdn','app',
        'mobile','m','secure','login','support',
        'help','forum','store','news','media',
        'images','static','assets','upload',
        'download','files','backup','old','new',
        'beta','alpha','demo','docs','wiki'
    ]

    found = []
    lock = threading.Lock()

    def check(sub):
        url = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(url)
            with lock:
                found.append((url, ip))
                print(f"✅ FOUND: {url} → {ip}")
        except:
            pass

    threads = []
    for sub in subdomains:
        t = threading.Thread(target=check, args=(sub,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"\n{'='*40}")
    print(f"Total found: {len(found)}")
    print(f"{'='*40}")
    return found

while True:
    domain = input("\nEnter domain (e.g. google.com)"
    " or 'quit': ")
    if domain == 'quit':
        break
    find_subdomains(domain)
