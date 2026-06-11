#!/bin/bash
echo "================================="
echo "  CYBER CELL AUTO RECON TOOL"
echo "  By Jayesh Goyal"
echo "================================="

read -p "Enter target domain: " TARGET

echo "\n[1] IP ADDRESS:"
host $TARGET | head -5

echo "\n[2] WHOIS:"
whois $TARGET | grep -E "Registrar:|Creation|Expiry|Country:" | head -10

echo "\n[3] DNS RECORDS:"
nslookup $TARGET

echo "\n[4] OPEN PORTS:"
nmap -F $TARGET 2>/dev/null

echo "\n[5] HTTP HEADERS:"
curl -I https://$TARGET 2>/dev/null | head -15

echo "\n[6] SSL CERTIFICATE:"
echo | openssl s_client -connect $TARGET:443 2>/dev/null | openssl x509 -noout -dates -subject 2>/dev/null

echo "\n================================="
echo "RECON COMPLETE FOR: $TARGET"
echo "================================="
