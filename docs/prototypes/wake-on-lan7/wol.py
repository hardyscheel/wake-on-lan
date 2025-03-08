import socket
import struct

def create_magic_packet(mac_address):
    # Remove any separators from the MAC address
    mac_address = mac_address.replace(":", "").replace("-", "").replace(".", "")
    if len(mac_address) != 12:
        raise ValueError("Invalid MAC address format")
    
    # Create the magic packet
    mac_bytes = bytes.fromhex(mac_address)
    magic_packet = b'\xff' * 6 + mac_bytes * 16
    return magic_packet

# Send the magic packet - use this for implementation
def send_magic_packet(mac_address, broadcast_ip='255.255.255.255', port=9, interface_ip=None):
    magic_packet = create_magic_packet(mac_address)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        if interface_ip:
            sock.bind((interface_ip, 0))
        sock.sendto(magic_packet, (broadcast_ip, port))

# Send the magic packet - use this for testing or console
def wake_up(mac_address, broadcast_ip='255.255.255.255', port=9, interface_ip=None):
    try:
        send_magic_packet(mac_address, broadcast_ip, port, interface_ip)
        print(f"Wake-on-LAN packet sent to: {mac_address} via {broadcast_ip}:{port} using interface {interface_ip}")
    except Exception as e:
        print(f"An error occurred: {e}")