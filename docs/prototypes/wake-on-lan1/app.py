'''
## Description
Send Wake-on-LAN packets to wake up sleeping devices in your network.
The app uses the wakeonlan Python module and a tkinter GUI.

The format of the MAC-addresses you can type in:
- ff.ff.ff.ff.ff.ff
- 00-00-00-00-00-00
- FFFFFFFFFFFF

## Requirements to run the app:
    pip install wakeonlan

## Further reading
[Usage of "wakeonlan" Python module](https://pypi.org/project/wakeonlan/)
[WakeOnLAN protocoll on Wikipedia](http://en.wikipedia.org/wiki/Wake-on-LAN)
'''

import tkinter as tk
from tkinter import messagebox
from wakeonlan import send_magic_packet

# Send Wake-on-LAN packet
def wake_up():
    mac_address = mac_entry.get()
    if not mac_address:
        messagebox.showerror("Error", "Please enter a MAC address.")
        return
    try:
        send_magic_packet(mac_address)
        messagebox.showinfo("Success", f"Wake-on-LAN packet sent to: {mac_address}")
    except Exception as e:
        messagebox.showerror("Error", f"An error has occurred: {e}")

# Create GUI
root = tk.Tk()
root.title("Wake-on-LAN")

# Label and input field for the MAC address
tk.Label(root, text="MAC-address:").grid(row=0, column=0, padx=10, pady=10)
mac_entry = tk.Entry(root, width=20)
mac_entry.grid(row=0, column=1, padx=10, pady=10)

# Send button
wake_button = tk.Button(root, text="Wake Up", command=wake_up)
wake_button.grid(row=1, column=0, columnspan=2, pady=10)

# Main loop of the GUI
root.mainloop()