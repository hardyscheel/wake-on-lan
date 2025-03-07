import tkinter as tk
from tkinter import messagebox
import socket
import struct

# Funktion zum Erstellen des Magic Packets
def create_magic_packet(mac_address):
    header = b'\xff' * 6
    mac_bytes = bytes.fromhex(mac_address.replace(':', ''))
    payload = mac_bytes * 16
    magic_packet = header + payload
    return magic_packet

# Funktion zum Senden des Magic Packets
def send_magic_packet(mac_address, broadcast_address='255.255.255.255', port=9):
    magic_packet = create_magic_packet(mac_address)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(magic_packet, (broadcast_address, port))
    sock.close()

# Funktion zum Aufwecken
def wake_up():
    mac_address = mac_entry.get()
    broadcast_address = broadcast_entry.get()
    
    if not mac_address or not broadcast_address:
        messagebox.showerror("Fehler", "Bitte gib eine MAC-Adresse und eine Broadcast-Adresse ein.")
        return
    
    try:
        send_magic_packet(mac_address, broadcast_address)
        messagebox.showinfo("Erfolg", f"Magic Packet an {mac_address} gesendet.")
    except Exception as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

# GUI erstellen
root = tk.Tk()
root.title("Wake-on-LAN Sender")

# Eingabefelder
tk.Label(root, text="MAC-Adresse:").grid(row=0, column=0, padx=10, pady=10)
mac_entry = tk.Entry(root, width=20)
mac_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Broadcast-Adresse:").grid(row=1, column=0, padx=10, pady=10)
broadcast_entry = tk.Entry(root, width=20)
broadcast_entry.grid(row=1, column=1, padx=10, pady=10)
broadcast_entry.insert(0, "255.255.255.255")  # Standard-Broadcast-Adresse

# Button zum Senden
wake_button = tk.Button(root, text="Wake Up", command=wake_up)
wake_button.grid(row=2, column=0, columnspan=2, pady=10)

# Hauptloop der GUI
root.mainloop()