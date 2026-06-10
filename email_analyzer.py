import re
import socket
from datetime import datetime

def analyze_headers(raw_headers):
    print("\n" + "="*45)
    print("   CYBER CELL EMAIL HEADER ANALYZER")
    print("   By Jayesh Goyal")
    print("="*45)

    # Extract IPs
    print("\n[1] IP ADDRESSES FOUND:")
    ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
    raw_headers)
    unique_ips = list(set(ips))
    if unique_ips:
        for ip in unique_ips:
            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except:
                hostname = "Unknown"
            print(f"    IP: {ip} → {hostname}")
    else:
        print("    No IPs found")

    # Extract From
    print("\n[2] SENDER INFO:")
    from_match = re.findall(
    r'From:.*', raw_headers, re.IGNORECASE)
    for f in from_match[:3]:
        print(f"    {f.strip()}")

    # Extract Reply-To
    print("\n[3] REPLY-TO:")
    reply = re.findall(
    r'Reply-To:.*', raw_headers, re.IGNORECASE)
    if reply:
        for r in reply:
            print(f"    {r.strip()}")
        # Check if From and Reply-To differ
        if from_match and reply:
            print("    ⚠️  WARNING: From and Reply-To")
            print("    are different — possible SPOOFING!")
    else:
        print("    None found")

    # Extract timestamps
    print("\n[4] TIMESTAMPS:")
    dates = re.findall(
    r'Date:.*', raw_headers, re.IGNORECASE)
    for d in dates[:3]:
        print(f"    {d.strip()}")

    # Extract mail servers
    print("\n[5] MAIL SERVERS (Received from):")
    received = re.findall(
    r'Received: from.*', raw_headers, re.IGNORECASE)
    for i, r in enumerate(received[:5]):
        print(f"    Hop {i+1}: {r.strip()[:60]}")

    # Extract message ID
    print("\n[6] MESSAGE ID:")
    msgid = re.findall(
    r'Message-ID:.*', raw_headers, re.IGNORECASE)
    for m in msgid:
        print(f"    {m.strip()}")

    # Spam indicators
    print("\n[7] SPAM/PHISHING INDICATORS:")
    indicators = []
    if 'X-Spam' in raw_headers:
        indicators.append("⚠️  Spam headers detected")
    if len(set(re.findall(
    r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
    raw_headers))) > 5:
        indicators.append("⚠️  Many different IPs — suspicious!")
    if reply and from_match:
        if reply[0] != from_match[0]:
            indicators.append("🚨 Reply-To differs from From!")
    if not indicators:
        indicators.append("✅ No obvious indicators found")
    for ind in indicators:
        print(f"    {ind}")

    print("\n" + "="*45)
    print("ANALYSIS COMPLETE!")
    print("="*45 + "\n")

print("CYBER CELL EMAIL HEADER ANALYZER")
print("Paste your email headers below.")
print("When done type 'END' on a new line:\n")

lines = []
while True:
    line = input()
    if line == 'END':
        break
    lines.append(line)

raw_headers = '\n'.join(lines)
if raw_headers.strip():
    analyze_headers(raw_headers)
else:
    print("No headers provided!")
