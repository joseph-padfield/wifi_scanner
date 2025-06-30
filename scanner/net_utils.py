# 1. Identify active network interface
# 2. Get IP address and subnet mask
# 3. Convert into CIDR notation

import netifaces
import ipaddress

def get_active_interface():
    for interface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface)

        if netifaces.AF_INET in addrs:
            for addr in addrs[netifaces.AF_INET]:
                ip = addr.get('addr')
                if ip and not ip.startswith('127.'):
                    return interface
    return None

def get_interface_info(interface):
    addrs = netifaces.ifaddresses(interface).get(netifaces.AF_INET)
    if not addrs:
        return None, None
    
    ip = addrs[0].get('addr')
    netmask = addrs[0].get('netmask')
    return ip, netmask

def get_cidr_range(ip, netmask):
    network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
    return str(network)

def detect_local_cidr():
    interface = get_active_interface()
    if not interface:
        raise RuntimeError("No active netork interface found.")
    
    ip, netmask = get_interface_info(interface)
    if not ip or not netmask:
        raise RuntimeError(f"Could not get IP/netmask for {interface}")
    
    cidr = get_cidr_range(ip, netmask)

    return {
        "interface": interface,
        "ip": ip,
        "netmask": netmask,
        "cidr": cidr
    }
