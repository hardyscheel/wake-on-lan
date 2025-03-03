'''
## Description
Send Wake-on-LAN packets to wake up sleeping devices in your network.
The app uses the wakeonlan Python module and a tkinter GUI.

The format of the MAC-addresses you can type in:
- ff.ff.ff.ff.ff.ff
- 00-00-00-00-00-00
- FFFFFFFFFFFF

You may need the IPv4-address of your network interface. Use `ipconfig` (Windows) or `ifconfig` (Linux) to determine your network interface ip-address.

## Requirements to run the app:
    pip install wakeonlan
    pip install psutil

## Further reading
[Usage of "wakeonlan" Python module](https://pypi.org/project/wakeonlan/)
[WakeOnLAN protocoll on Wikipedia](http://en.wikipedia.org/wiki/Wake-on-LAN)
[Tkinter Tutorials on pythontutorial.net](https://www.pythontutorial.net/tkinter/)
'''

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk   # ttk for Treeview
from wakeonlan import send_magic_packet
import json
import os
import psutil  # Zum Ermitteln der Netzwerkschnittstellen

# Datei zum Speichern der MAC-Adressen
DATA_FILE = "mac_addresses.json"

# Funktion zum Laden der MAC-Adressen aus der Datei
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

# Funktion zum Speichern der MAC-Adressen in der Datei
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Funktion zum Hinzufügen eines neuen Eintrags
def add_entry():
    name = name_entry.get()
    mac = mac_entry.get()
    if not name or not mac:
        messagebox.showerror("Fehler", "Bitte gib sowohl einen Namen als auch eine MAC-Adresse ein.")
        return
    data.append({"name": name, "mac": mac})
    save_data(data)
    update_table()
    name_entry.delete(0, tk.END)
    mac_entry.delete(0, tk.END)

# Edit an entry
def edit_entry():
    selected_item = mac_table.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a row to edit.")
        return
    index = int(mac_table.item(selected_item, "values")[0])
    entry = data[index]
    new_name = simpledialog.askstring("Edit", "New Name:", initialvalue=entry["name"])
    new_mac = simpledialog.askstring("Edit", "New MAC Address:", initialvalue=entry["mac"])
    if new_name and new_mac:
        data[index] = {"name": new_name, "mac": new_mac}
        save_data(data)
        update_table()

# Delete an entry
def delete_entry():
    selected_item = mac_table.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a row to delete.")
        return
    index = int(mac_table.item(selected_item, "values")[0])
    data.pop(index)
    save_data(data)
    update_table()

# Funktion zum Aufwecken eines Eintrags
def wake_entry():
    selected_mac = mac_table.selection()
    if not selected_mac:
        messagebox.showerror("Error", "Please select a row to wake.")
        return    
    mac = mac_table.item(selected_mac, "values")[2]
    ip = False

    if interface_table.selection():
        ip = interface_table.item(interface_table.selection())["values"][1]  # IP der ausgewählten Schnittstelle

    try:
        if mac and ip:
            send_magic_packet(mac, interface=ip)  # Interface-IP angeben
            messagebox.showinfo("Success", f"Wake-on-LAN packet sent to: {mac} via interface {ip}")
        else:
            send_magic_packet(mac)
            messagebox.showinfo("Success", f"Wake-on-LAN packet sent to: {mac}")
    except Exception as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

# Funktion zum Aktualisieren der MAC-Tabelle
def update_table():
    for row in mac_table.get_children():
        mac_table.delete(row)
    for i, entry in enumerate(data):
        mac_table.insert("", "end", values=(i, entry["name"], entry["mac"]))

# Funktion zum Ermitteln der Netzwerkschnittstellen
def get_network_interfaces():
    interfaces = []
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == 2:  # AF_INET entspricht dem numerischen Wert 2 (IPv4)
                interfaces.append((interface, addr.address))
    return interfaces

# Funktion zum Aktualisieren der Interface-Tabelle
def update_interface_table():
    for row in interface_table.get_children():
        interface_table.delete(row)
    for interface, ip in get_network_interfaces():
        interface_table.insert("", "end", values=(interface, ip))

# GUI erstellen
root = tk.Tk()
root.title("Wake-on-LAN")

# Input fields for new entry
tk.Label(root, text="Name:").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(root, width=20)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="MAC Address:").grid(row=0, column=2, padx=5, pady=5)
mac_entry = tk.Entry(root, width=20)
mac_entry.grid(row=0, column=3, padx=5, pady=5)

add_button = tk.Button(root, text="Add", command=add_entry)
add_button.grid(row=0, column=4, padx=5, pady=5)

# Table for existing entries
columns = ("Index", "Name", "MAC Address")
mac_table = ttk.Treeview(root, columns=columns, show="headings")
mac_table.heading("Index", text="Index")
mac_table.heading("Name", text="Name")
mac_table.heading("MAC Address", text="MAC Address")
mac_table.column("Index", width=50)
mac_table.column("Name", width=150)
mac_table.column("MAC Address", width=150)
mac_table.grid(row=1, column=0, columnspan=5, padx=5, pady=10)

# Buttons for actions
button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, columnspan=5, pady=10)

wake_button = tk.Button(button_frame, text="Wake", command=wake_entry)
wake_button.pack(side=tk.LEFT, padx=10)

edit_button = tk.Button(button_frame, text="Edit", command=edit_entry)
edit_button.pack(side=tk.LEFT, padx=10)

delete_button = tk.Button(button_frame, text="Delete", command=delete_entry)
delete_button.pack(side=tk.LEFT, padx=10)

# Tabelle für Netzwerkschnittstellen
interface_columns = ("Interface", "IP-Adresse")
interface_table = ttk.Treeview(root, columns=interface_columns, show="headings")
interface_table.heading("Interface", text="Interface")
interface_table.heading("IP-Adresse", text="IP-Adresse")
interface_table.grid(row=3, column=0, columnspan=5, padx=10, pady=10)

# Daten laden und Tabellen aktualisieren
data = load_data()
update_table()
update_interface_table()

# Hauptloop der GUI
root.mainloop()