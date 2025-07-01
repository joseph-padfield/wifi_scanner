import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scanner.net_utils import detect_local_cidr
from scanner.arp_scanner import arp_scan

if __name__ == "__main__":
    info = detect_local_cidr()
    print(f"Scanning: {info['cidr']} on {info['interface']}")
    devices = arp_scan(info['cidr'])

    print(f"\nFound {len(devices)} device(s):\n")
    print("IP Address\t\tMAC Address")
    print('-' * 40)
    for d in devices:
        print(f"{d['ip']:<16}\t{d['mac']}")