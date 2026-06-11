#!/bin/bash
echo "=== CYBER CELL LINUX PRACTICE ==="
echo "By Jayesh Goyal"
echo "================================="

echo "\n[1] System Info:"
uname -a

echo "\n[2] Current User:"
whoami

echo "\n[3] All Running Processes:"
ps aux | head -20

echo "\n[4] Network Connections:"
netstat -tuln 2>/dev/null || ss -tuln

echo "\n[5] Open Files:"
ls -la /proc/*/fd 2>/dev/null | head -20

echo "\n[6] Disk Usage:"
df -h

echo "\n[7] Memory Usage:"
free -h 2>/dev/null || cat /proc/meminfo | head -10

echo "\n[8] Recent Commands:"
history | tail -20

echo "\n[9] All Users:"
cat /etc/passwd | cut -d: -f1

echo "\n[10] Environment Variables:"
env | grep -i path

echo "\n================================="
echo "SCAN COMPLETE!"
