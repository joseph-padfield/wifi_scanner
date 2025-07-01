from scapy.all import ARP, Ether, srp

def arp_scan(cidr_range, timeout=2):
    """
    Performs an ARP scan on the given CIDR range.

    Args:
        cidr_range (str): Network range in CIDR format (e.g. '192.168.0.0/24').
        timeout (int): How long to wait for responses (seconds).

    Returns:
        List[Dict]: List of dictionaries with 'ip' and 'mac' keys.
    """
    # Construct ARP packet
    arp = ARP(pdst=cidr_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff") # Broadcast MAC
    packet = ether / arp

    # Send the packet and receive responses
    answered, _ = srp(packet, timeout=timeout, verbose=0)

    # Extract device info
    devices = []
    for _, received in answered:
        devices.append({
            "ip": received.psrc,
            "mac": received.hwsrc
        })

    return devices