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

# File to store MAC addresses
DATA_FILE = "mac_addresses.json"

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
    selected_item = table.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a row to edit.")
        return
    index = int(table.item(selected_item, "values")[0])
    entry = data[index]
    new_name = simpledialog.askstring("Edit", "New Name:", initialvalue=entry["name"])
    new_mac = simpledialog.askstring("Edit", "New MAC Address:", initialvalue=entry["mac"])
    if new_name and new_mac:
        data[index] = {"name": new_name, "mac": new_mac}
        save_data(data)
        update_table()

# Delete an entry
def delete_entry():
    selected_item = table.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a row to delete.")
        return
    index = int(table.item(selected_item, "values")[0])
    data.pop(index)
    save_data(data)
    update_table()

# Wake an entry
def wake_entry():
    selected_item = table.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a row to wake.")
        return
    mac = table.item(selected_item, "values")[2]
    ip_address = ip_entry.get()  # Get the IPv4 address from the input field

    try:
        if ip_address:
            send_magic_packet(mac, interface=ip_address)
            messagebox.showinfo("Success", f"Wake-on-LAN packet sent to: {mac} via interface {ip_address}")
        else:
            send_magic_packet(mac)
            messagebox.showinfo("Success", f"Wake-on-LAN packet sent to: {mac}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Update the table
def update_table():
    # Clear the table
    for row in table.get_children():
        table.delete(row)
    
    # Insert new rows
    for i, entry in enumerate(data):
        table.insert("", "end", values=(i, entry["name"], entry["mac"]))

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

# Label and input field for the IPv4 address of the network interface to be used.
tk.Label(root, text="interface address (optional):").grid(row=1, column=1, padx=5, pady=5)
ip_entry = tk.Entry(root, width=20)
ip_entry.grid(row=1, column=2, padx=5, pady=5)

# Table for existing entries
columns = ("Index", "Name", "MAC Address")
table = ttk.Treeview(root, columns=columns, show="headings")
table.heading("Index", text="Index")
table.heading("Name", text="Name")
table.heading("MAC Address", text="MAC Address")
table.column("Index", width=50)
table.column("Name", width=150)
table.column("MAC Address", width=150)
table.grid(row=2, column=0, columnspan=5, padx=5, pady=10)

# Buttons for actions
button_frame = tk.Frame(root)
button_frame.grid(row=3, column=0, columnspan=5, pady=10)

wake_button = tk.Button(button_frame, text="Wake", command=wake_entry)
wake_button.pack(side=tk.LEFT, padx=10)

edit_button = tk.Button(button_frame, text="Edit", command=edit_entry)
edit_button.pack(side=tk.LEFT, padx=10)

delete_button = tk.Button(button_frame, text="Delete", command=delete_entry)
delete_button.pack(side=tk.LEFT, padx=10)

# Load data and update the table
data = load_data()
update_table()

# Main loop of the GUI
root.mainloop()