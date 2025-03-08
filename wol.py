import socket
import argparse

def create_magic_packet(mac_address):
    """
    Creates a Wake-on-LAN Magic Packet for the specified MAC address.
    
    :param mac_address: The MAC address of the target device (e.g., "00:11:22:33:44:55").
    :return: The Magic Packet as a byte object.
    """
    # Remove separators from the MAC address
    mac_address = mac_address.replace(":", "").replace("-", "").replace(".", "")
    if len(mac_address) != 12:
        raise ValueError("Invalid MAC address format")
    
    # Create the Magic Packet
    mac_bytes = bytes.fromhex(mac_address)
    magic_packet = b'\xff' * 6 + mac_bytes * 16
    return magic_packet

def send_magic_packet(mac_address, broadcast_ip='255.255.255.255', port=9, interface_ip=None):
    """
    Sends a Wake-on-LAN Magic Packet to the specified MAC address.
    
    :param mac_address: The MAC address of the target device.
    :param broadcast_ip: The broadcast IP address (default: 255.255.255.255).
    :param port: The target port (default: 9).
    :param interface_ip: The IP address of the network interface (optional).
    """
    magic_packet = create_magic_packet(mac_address)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        if interface_ip:
            sock.bind((interface_ip, 0))  # Bind to the specific interface
        sock.sendto(magic_packet, (broadcast_ip, port))

def wake_up(mac_address, broadcast_ip='255.255.255.255', port=9, interface_ip=None):
    """
    Sends a Wake-on-LAN Magic Packet and prints a success message.
    
    :param mac_address: The MAC address of the target device.
    :param broadcast_ip: The broadcast IP address (default: 255.255.255.255).
    :param port: The target port (default: 9).
    :param interface_ip: The IP address of the network interface (optional).
    """
    try:
        send_magic_packet(mac_address, broadcast_ip, port, interface_ip)
        print(f"Wake-on-LAN packet sent to: {mac_address} via {broadcast_ip}:{port} (Interface: {interface_ip})")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    """
    Main function for using the script via the console.
    """
    parser = argparse.ArgumentParser(description="Sends a Wake-on-LAN Magic Packet.")
    parser.add_argument("mac_address", help="The MAC address of the target device (e.g., 00:11:22:33:44:55).")
    parser.add_argument("--broadcast_ip", default="255.255.255.255", help="The broadcast IP address (default: 255.255.255.255).")
    parser.add_argument("--port", type=int, default=9, help="The target port (default: 9).")
    parser.add_argument("--interface_ip", help="The IP address of the network interface (optional).")
    
    args = parser.parse_args()
    
    # Send the Magic Packet
    wake_up(args.mac_address, args.broadcast_ip, args.port, args.interface_ip)

if __name__ == "__main__":
    main()