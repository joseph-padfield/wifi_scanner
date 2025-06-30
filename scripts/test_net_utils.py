import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scanner import net_utils

if __name__ == "__main__":
    info = net_utils.detect_local_cidr()
    print("Your local network info:")
    print(f"Interface: {info['interface']}")
    print(f"IP: {info['ip']}")
    print(f"Netmask: {info['netmask']}")
    print(f"CIDR: {info['cidr']}")