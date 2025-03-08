import tkinter as tk
from tkinter import messagebox
import socket
import struct

# Function to create the Magic Packet
def create_magic_packet(mac_address):
    header = b'\xff' * 6
    mac_bytes = bytes.fromhex(mac_address.replace(':', ''))
    payload = mac_bytes * 16
    magic_packet = header + payload
    return magic_packet

# Function to send the Magic Packet
def send_magic_packet(mac_address, broadcast_address='255.255.255.255', port=9, interface=None):
    magic_packet = create_magic_packet(mac_address)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if interface:
        sock.bind((interface, 0))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(magic_packet, (broadcast_address, port))
    sock.close()

# Function to wake up
def wake_up():
    mac_address = mac_entry.get()
    broadcast_address = broadcast_entry.get()
    interface = interface_entry.get()
    
    if not mac_address or not broadcast_address:
        messagebox.showerror("Error", "Please enter a MAC address and a broadcast address.")
        return
    
    try:
        send_magic_packet(mac_address, broadcast_address, interface=interface)
        messagebox.showinfo("Success", f"Magic Packet sent to {mac_address}.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create GUI
root = tk.Tk()
root.title("Wake-on-LAN Sender")

# Input fields
tk.Label(root, text="MAC Address:").grid(row=0, column=0, padx=10, pady=10)
mac_entry = tk.Entry(root, width=20)
mac_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Broadcast Address:").grid(row=1, column=0, padx=10, pady=10)
broadcast_entry = tk.Entry(root, width=20)
broadcast_entry.grid(row=1, column=1, padx=10, pady=10)
broadcast_entry.insert(0, "255.255.255.255")  # Default broadcast address

tk.Label(root, text="Interface Address:").grid(row=2, column=0, padx=10, pady=10)
interface_entry = tk.Entry(root, width=20)
interface_entry.grid(row=2, column=1, padx=10, pady=10)

# Button to send
wake_button = tk.Button(root, text="Wake Up", command=wake_up)
wake_button.grid(row=3, column=0, columnspan=2, pady=10)

# Main loop of the GUI
root.mainloop()