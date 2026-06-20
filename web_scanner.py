import requests
import re
import socket
import ssl
import datetime
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings()

# ============================================
#   PROFESSIONAL WEB VULNERABILITY SCANNER
#   By Jayesh Goyal | zer0day.tech
#   For authorized security audits only
# ============================================

BANNER = """
╔══════════════════════════════════════════╗
║   PROFESSIONAL WEB VULNERABILITY SCANNER ║
║   By Jayesh Goyal | zer0day.tech         ║
║   Use only with written permission!      ║
╚══════════════════════════════════════════╝
"""

class WebScanner:
    def __init__(self, target):
        self.target = target
        if not target.startswith('http'):
            self.target = 'https://' + target
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 Security Audit Bot'
        }
        self.vulnerabilities = []
        self.info = []
        self.start_time = datetime.datetime.now()

    def log_vuln(self, severity, title, detail):
        self.vulnerabilities.append({
            'severity': severity,
            'title': title,
            'detail': detail
        })
        icon = {'CRITICAL':'🚨','HIGH':'❌',
        'MEDIUM':'⚠️','LOW':'💡'}
        print(f"\n{icon.get(severity,'▸')} "
        f"[{severity}] {title}")
        print(f"   {detail}")

    def log_info(self, title, detail):
        self.info.append(f"{title}: {detail}")
        print(f"\n[ℹ️] {title}: {detail}")

    # ── 1. Basic Info ─────────────────────
    def get_basic_info(self):
        print("\n[*] Gathering basic information...")
        try:
            r = self.session.get(
            self.target, timeout=10,
            verify=False)
            self.log_info("Status Code",
            str(r.status_code))
            self.log_info("Server",
            r.headers.get('server','Unknown'))
            self.log_info("Content Type",
            r.headers.get('content-type','Unknown'))

            # X-Powered-By reveals tech stack
            if 'x-powered-by' in r.headers:
                self.log_vuln('MEDIUM',
                'Technology Disclosure',
                f"X-Powered-By: "
                f"{r.headers['x-powered-by']} "
                f"— Reveals server technology!")

            return r
        except Exception as e:
            print(f"   Error: {e}")
            return None

    # ── 2. Security Headers ───────────────
    def check_security_headers(self):
        print("\n[*] Checking security headers...")
        try:
            r = self.session.get(
            self.target, timeout=10,
            verify=False)
            headers = r.headers

            required = {
                'x-frame-options':
                'Clickjacking protection missing!',
                'x-xss-protection':
                'XSS protection header missing!',
                'x-content-type-options':
                'MIME sniffing protection missing!',
                'content-security-policy':
                'CSP header missing — XSS risk!',
                'strict-transport-security':
                'HSTS missing — SSL stripping risk!',
                'referrer-policy':
                'Referrer policy missing!'
            }

            for header, msg in required.items():
                if header not in [
                h.lower() for h in headers]:
                    severity = 'HIGH' if header in [
                    'content-security-policy',
                    'strict-transport-security'
                    ] else 'MEDIUM'
                    self.log_vuln(severity,
                    f'Missing Header: {header}',msg)
                else:
                    print(f"   ✅ {header} present")

        except Exception as e:
            print(f"   Error: {e}")

    # ── 3. SQL Injection ──────────────────
    def check_sql_injection(self):
        print("\n[*] Testing SQL injection...")
        payloads = [
            "'", "''", "`", "``",
            "' OR '1'='1", "' OR 1=1--",
            "' OR 'x'='x", "1' ORDER BY 1--",
            "1' ORDER BY 2--",
            "' UNION SELECT NULL--",
            "admin'--", "1 OR 1=1",
        ]
        sql_errors = [
            'sql syntax', 'mysql_fetch',
            'ora-01756', 'sqlite_error',
            'postgresql', 'warning: mysql',
            'valid mysql result',
            'you have an error in your sql',
            'mysql_num_rows','mssql_',
            'odbc_','jdbc error',
            'syntax error','unclosed quotation'
        ]
        try:
            # Test URL parameters
            r = self.session.get(
            self.target, timeout=10,
            verify=False)
            soup = BeautifulSoup(
            r.text, 'html.parser')

            # Find forms
            forms = soup.find_all('form')
            print(f"   Found {len(forms)} forms")

            for i, form in enumerate(forms):
                action = form.get('action','')
                method = form.get('method','get')
                inputs = form.find_all('input')

                for payload in payloads[:5]:
                    data = {}
                    for inp in inputs:
                        name = inp.get('name','')
                        if name:
                            data[name] = payload

                    try:
                        if method.lower() == 'post':
                            resp = self.session.post(
                            urljoin(self.target,action),
                            data=data, timeout=8,
                            verify=False)
                        else:
                            resp = self.session.get(
                            urljoin(self.target,action),
                            params=data, timeout=8,
                            verify=False)

                        for err in sql_errors:
                            if err in resp.text.lower():
                                self.log_vuln('CRITICAL',
                                'SQL Injection Found!',
                                f"Form {i+1} vulnerable "
                                f"with payload: {payload}")
                                break
                    except:
                        pass

            # Test URL params directly
            test_urls = [
                f"{self.target}?id='",
                f"{self.target}?id=1'",
                f"{self.target}?page='",
                f"{self.target}?cat=1'"
            ]
            for url in test_urls:
                try:
                    resp = self.session.get(
                    url, timeout=5, verify=False)
                    for err in sql_errors:
                        if err in resp.text.lower():
                            self.log_vuln('CRITICAL',
                            'SQL Injection in URL!',
                            f"URL parameter vulnerable: "
                            f"{url}")
                            break
                except:
                    pass

        except Exception as e:
            print(f"   Error: {e}")

    # ── 4. XSS Testing ───────────────────
    def check_xss(self):
        print("\n[*] Testing XSS vulnerabilities...")
        payloads = [
            '<script>alert(1)</script>',
            '"><script>alert(1)</script>',
            '<img src=x onerror=alert(1)>',
            "';alert(1)//",
            '<svg onload=alert(1)>',
            '"><img src=x onerror=alert(1)>',
        ]
        try:
            r = self.session.get(
            self.target, timeout=10,
            verify=False)
            soup = BeautifulSoup(
            r.text, 'html.parser')
            forms = soup.find_all('form')

            for i, form in enumerate(forms):
                action = form.get('action','')
                method = form.get('method','get')
                inputs = form.find_all('input')

                for payload in payloads[:3]:
                    data = {}
                    for inp in inputs:
                        name = inp.get('name','')
                        if name:
                            data[name] = payload
                    try:
                        if method.lower() == 'post':
                            resp = self.session.post(
                            urljoin(self.target,action),
                            data=data, timeout=8,
                            verify=False)
                        else:
                            resp = self.session.get(
                            urljoin(self.target,action),
                            params=data, timeout=8,
                            verify=False)

                        if payload in resp.text:
                            self.log_vuln('HIGH',
                            'XSS Vulnerability Found!',
                            f"Form {i+1} reflects "
                            f"XSS payload: {payload[:30]}")
                    except:
                        pass

        except Exception as e:
            print(f"   Error: {e}")

    # ── 5. Directory Traversal ────────────
    def check_sensitive_files(self):
        print("\n[*] Checking exposed files...")
        sensitive = [
            '/robots.txt', '/.git/HEAD',
            '/.env', '/config.php',
            '/wp-config.php', '/admin/',
            '/administrator/', '/phpmyadmin/',
            '/.htaccess', '/backup/',
            '/db.sql', '/database.sql',
            '/config/', '/conf/',
            '/test/', '/dev/',
            '/.DS_Store', '/web.config',
            '/crossdomain.xml',
            '/sitemap.xml',
            '/api/', '/api/v1/',
            '/.git/config',
            '/server-status',
        ]
        found = []
        for path in sensitive:
            try:
                url = self.target.rstrip('/') + path
                r = self.session.get(
                url, timeout=5, verify=False,
                allow_redirects=False)
                if r.status_code == 200:
                    severity = 'CRITICAL' if path in [
                    '/.env','/.git/HEAD',
                    '/wp-config.php',
                    '/.git/config','/db.sql'
                    ] else 'MEDIUM'
                    self.log_vuln(severity,
                    f'Exposed: {path}',
                    f"File accessible at {url} "
                    f"— Status: {r.status_code}")
                    found.append(path)
            except:
                pass
        if not found:
            print("   ✅ No sensitive files exposed")

    # ── 6. SSL Check ─────────────────────
    def check_ssl(self):
        print("\n[*] Checking SSL/TLS...")
        try:
            hostname = urlparse(
            self.target).hostname
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(
            socket.socket(),
            server_hostname=hostname) as s:
                s.settimeout(5)
                s.connect((hostname, 443))
                cert = s.getpeercert()
                expire = datetime.datetime.strptime(
                cert['notAfter'],
                '%b %d %H:%M:%S %Y %Z')
                days_left = (
                expire - datetime.datetime.now()
                ).days
                self.log_info("SSL Expires",
                f"{expire.date()} "
                f"({days_left} days left)")
                if days_left < 30:
                    self.log_vuln('HIGH',
                    'SSL Expiring Soon!',
                    f"Certificate expires in "
                    f"{days_left} days!")
                else:
                    print(f"   ✅ SSL valid for "
                    f"{days_left} days")
        except ssl.SSLError as e:
            self.log_vuln('CRITICAL',
            'SSL Error!', str(e))
        except Exception as e:
            print(f"   SSL check: {e}")

    # ── 7. Open Ports ─────────────────────
    def check_ports(self):
        print("\n[*] Checking common ports...")
        hostname = urlparse(
        self.target).hostname
        dangerous_ports = {
            21:'FTP',22:'SSH',23:'Telnet⚠️',
            25:'SMTP',80:'HTTP',443:'HTTPS',
            3306:'MySQL⚠️',5432:'PostgreSQL⚠️',
            6379:'Redis⚠️',27017:'MongoDB⚠️',
            8080:'HTTP-Alt',8443:'HTTPS-Alt',
            9200:'Elasticsearch⚠️',
        }
        try:
            ip = socket.gethostbyname(hostname)
            self.log_info("Target IP", ip)
            for port, service in \
            dangerous_ports.items():
                s = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM)
                s.settimeout(0.8)
                result = s.connect_ex(
                (ip, port))
                s.close()
                if result == 0:
                    if '⚠️' in service:
                        self.log_vuln('HIGH',
                        f'Dangerous Port Open: '
                        f'{port}',
                        f"{service} port is open "
                        f"— should not be public!")
                    else:
                        print(f"   ✅ Port {port} "
                        f"({service}) open — normal")
        except Exception as e:
            print(f"   Error: {e}")

    # ── 8. Generate Report ────────────────
    def generate_report(self):
        end_time = datetime.datetime.now()
        duration = (end_time -
        self.start_time).seconds

        critical = [v for v in
        self.vulnerabilities
        if v['severity']=='CRITICAL']
        high = [v for v in
        self.vulnerabilities
        if v['severity']=='HIGH']
        medium = [v for v in
        self.vulnerabilities
        if v['severity']=='MEDIUM']
        low = [v for v in
        self.vulnerabilities
        if v['severity']=='LOW']

        report = f"""
╔══════════════════════════════════════════╗
║         SECURITY AUDIT REPORT           ║
╠══════════════════════════════════════════╣
║ Target:   {self.target[:40]:<40} ║
║ Date:     {str(end_time.date()):<40} ║
║ Duration: {str(duration)+' seconds':<40} ║
║ Auditor:  Jayesh Goyal | zer0day.tech   ║
╠══════════════════════════════════════════╣
║ VULNERABILITY SUMMARY                   ║
║ 🚨 Critical: {str(len(critical)):<28} ║
║ ❌ High:     {str(len(high)):<28} ║
║ ⚠️  Medium:  {str(len(medium)):<28} ║
║ 💡 Low:      {str(len(low)):<28} ║
║ Total:       {str(len(self.vulnerabilities)):<28} ║
╠══════════════════════════════════════════╣
║ RISK RATING                             ║"""

        if critical:
            report += "\n║ 🚨 CRITICAL RISK                        ║"
        elif high:
            report += "\n║ ❌ HIGH RISK                             ║"
        elif medium:
            report += "\n║ ⚠️  MEDIUM RISK                          ║"
        else:
            report += "\n║ ✅ LOW RISK                              ║"

        report += """
╠══════════════════════════════════════════╣
║ DETAILED FINDINGS                       ║
╚══════════════════════════════════════════╝
"""
        for v in self.vulnerabilities:
            icon = {'CRITICAL':'🚨','HIGH':'❌',
            'MEDIUM':'⚠️','LOW':'💡'}
            report += f"""
[{v['severity']}] {icon.get(v['severity'],'▸')} {v['title']}
Detail: {v['detail']}
{'─'*44}"""

        report += f"""

╔══════════════════════════════════════════╗
║ RECOMMENDATIONS                         ║
╠══════════════════════════════════════════╣
║ 1. Fix CRITICAL issues immediately      ║
║ 2. Address HIGH issues within 24 hours  ║
║ 3. Fix MEDIUM issues within 1 week      ║
║ 4. Review LOW issues within 1 month     ║
║ 5. Re-scan after fixes are applied      ║
╠══════════════════════════════════════════╣
║ DISCLAIMER                              ║
║ This scan was performed with            ║
║ authorized permission only.             ║
║ Report is confidential.                 ║
╚══════════════════════════════════════════╝

Generated by: Jayesh Goyal
Website: zer0day.tech
GitHub: github.com/jayesh-goyal/cyber-toolkit
Date: {end_time}
"""
        print(report)

        # Save report
        filename = f"report_{urlparse(self.target).hostname}_{end_time.strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            f.write(report)
        print(f"\n✅ Report saved: {filename}")
        return report

    # ── Run Full Scan ─────────────────────
    def run(self):
        print(BANNER)
        print(f"Target: {self.target}")
        print(f"Started: {self.start_time}")
        print("\n⚠️  Only scan with written permission!")
        confirm = input(
        "\nDo you have permission? (yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ Scan cancelled!")
            print("Always get written permission"
            " before scanning!")
            return

        print("\n" + "="*44)
        print("STARTING FULL SECURITY AUDIT...")
        print("="*44)

        self.get_basic_info()
        self.check_security_headers()
        self.check_sql_injection()
        self.check_xss()
        self.check_sensitive_files()
        self.check_ssl()
        self.check_ports()
        self.generate_report()

# ── Main ──────────────────────────────────
if __name__ == '__main__':
    print(BANNER)
    print("Professional Web Vulnerability Scanner")
    print("For authorized security audits only!\n")

    target = input("Enter target URL or domain: ")
    scanner = WebScanner(target)
    scanner.run()
