import tkinter as tk
from tkinter import messagebox, simpledialog, ttk  # ttk for Treeview
import json
import os
import psutil  # For retrieving network interfaces
from wol import wake_up  # Import the wake_up function

# File to store MAC addresses
DATA_FILE = "config/mac_addresses.json"

# Load MAC addresses from file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

# Save MAC addresses to file
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Add a new entry
def add_entry():
    name = name_entry.get()
    mac = mac_entry.get()
    if not name or not mac:
        messagebox.showerror("Error", "Please enter both a name and a MAC address.")
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

# Wake an entry
def wake_entry():
    selected_mac = mac_table.selection()
    if not selected_mac:
        messagebox.showerror("Error", "Please select a row to wake.")
        return    
    mac = mac_table.item(selected_mac, "values")[2]
    broadcast_ip = broadcast_ip_entry.get()
    port = port_entry.get()
    interface_ip = None

    if interface_table.selection():
        interface_ip = interface_table.item(interface_table.selection())["values"][1]  # IP of the selected interface

    if not broadcast_ip:
        broadcast_ip = '255.255.255.255'
    if not port:
        port = 9
    else:
        port = int(port)

    try:
        wake_up(mac, broadcast_ip, port, interface_ip)  # Use the wake_up function
        messagebox.showinfo("Success", f"Wake-on-LAN packet sent to: {mac} via {broadcast_ip}:{port} using interface {interface_ip}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Update the MAC table
def update_table():
    for row in mac_table.get_children():
        mac_table.delete(row)
    for i, entry in enumerate(data):
        mac_table.insert("", "end", values=(i, entry["name"], entry["mac"]))

# Retrieve network interfaces
def get_network_interfaces():
    interfaces = []
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == 2:  # psutil.AF_INET corresponds to the numeric value 2 (IPv4) because of changes in the new version of psutil
                interfaces.append((interface, addr.address))
    return interfaces

# Update the interface table
def update_interface_table():
    for row in interface_table.get_children():
        interface_table.delete(row)
    for interface, ip in get_network_interfaces():
        interface_table.insert("", "end", values=(interface, ip))

# Create the GUI
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

# Table for network interfaces
interface_columns = ("Interface", "IP Address")
interface_table = ttk.Treeview(root, columns=interface_columns, show="headings")
interface_table.heading("Interface", text="Interface")
interface_table.heading("IP Address", text="IP Address")
interface_table.grid(row=3, column=0, columnspan=5, padx=10, pady=10)

# Input fields for broadcast IP and port
tk.Label(root, text="Broadcast IP:").grid(row=4, column=0, padx=5, pady=5)
broadcast_ip_entry = tk.Entry(root, width=20)
broadcast_ip_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(root, text="Port:").grid(row=4, column=2, padx=5, pady=5)
port_entry = tk.Entry(root, width=20)
port_entry.grid(row=4, column=3, padx=5, pady=5)

# Load data and update tables
data = load_data()
update_table()
update_interface_table()

# Main loop of the GUI
root.mainloop()