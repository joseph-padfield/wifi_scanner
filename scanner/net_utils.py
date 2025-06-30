# 1. Identify active network interface
# 2. Get IP address and subnet mask
# 3. Convert into CIDR notation

import netifaces # lets you introspect system-level networking info
import ipaddress

def get_active_interface():
    """
    Detects and returns the name of the first active, non-loopback network interface.

    Returns:
        str: The name of the active interface (e.g. 'en0', 'eth0'), or None if none found.
    """
    for interface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface)

        if netifaces.AF_INET in addrs:
            for addr in addrs[netifaces.AF_INET]:
                ip = addr.get('addr')
                if ip and not ip.startswith('127.'):
                    return interface
    return None

def get_interface_info(interface):
    """
    Rretrieves the IPv4 address and subnet mask for a given network interface.

    Args:
        interface (str): Name of the network interface.

    Returns:
        tuple: (ip_address, subnet_mask) as strings, or (None, None) if not available.
    """
    addrs = netifaces.ifaddresses(interface).get(netifaces.AF_INET)
    if not addrs:
        return None, None
    
    ip = addrs[0].get('addr')
    netmask = addrs[0].get('netmask')
    return ip, netmask

def get_cidr_range(ip, netmask):
    """
    Converts an IP address and subnet mask to CIDR notation.

    Args:
        ip (str): The IPv4 address (e.g. '192.168.0.2')
        netmask (str): The subnet mask (e.g. '255.255.255.0')

    Returns:
        str: The network in CIDR notation (e.g. '192.168.0.0/24')
    """
    network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
    return str(network)

def detect_local_cidr():
    """
    Detects the local network CIDR range by:
        1. Finding the active interface.
        2. Getting the IP address and subnet mask.
        3. Converting to CIDR notation.

    Returns:
        dict: A dictionary containing:
            - interface (str): The active network interface name.
            - ip (str): The local IP address.
            - netmask (str): The subnet mask.
            - cidr (str): The CIDR range.

    Raises:
        RunTimeError: If no active interface is found or IP/netmask cannot be retrieved.
    """
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
