# wake-on-lan
A Wake-on-LAN Python module and GUI to use the Wake-on-LAN protocol to wake up sleeping network devices in your LAN.

**wake-on-lan** can be used as:
- an importable module
- can be called directly via console
- can be used as a standalone script
- there is also a GUI version

[README-images-01]: /docs/img/screenshot_main_window.png "Screenshot of the main window"
![README-images-01][README-images-01]

## Description
This Wake-on-LAN app is broadcasting Wake-on-LAN frames to wake up sleeping devices. Standard broadcast ip is 255.255.255.255 on Standard port 9. The broadcast ip and port can be changed. You can manage manage and store several mac addresses. Your computers network interfaces can be listed from where you can choose the right one you want to send Wake-on-LAN frames from.

## Requirements to run the app
    pip install psutil

## Usage 

### **Modul Usage**:
   - The functions `create_magic_packet`, `send_magic_packet`, and `wake_up` can be imported into other scripts, e.g.:
     ```python
     from wol import wake_up
     wake_up("00:11:22:33:44:55", broadcast_ip="192.168.1.255")
     ```

### **Usage via the Console:**

**Console Usage**:
   - Example 1: Simple call with MAC address:
     ```bash
     python wol.py 00:11:22:33:44:55
     ```
   - Example 2: With specific broadcast IP and interface IP:
     ```bash
     python wol.py 00:11:22:33:44:55 --broadcast_ip 192.168.1.255 --interface_ip 192.168.1.100
     ```

The format of the MAC-addresses you can use must be in one of the following format:
- ff.ff.ff.ff.ff.ff
- 00-00-00-00-00-00
- FFFFFFFFFFFF
- ff:ff:ff:ff:ff:ff

### GUI: How to use the GUI version of the app
1. Add one or more destination MAC-addresses of your devices you want to wake up. You can also add names for them and edit or delete them later.
2. Select a MAC-address/device from the table.
3. (Optional) Select a network interface of your computer. Your sleeping device must be in the same network as your network interface.
4. (Optional) Change the broadcast ip address and the port. Standard broadcast ip is 255.255.255.255 on Standard port is 9.


## Troubleshooting
**I need more information about my network interface!**  
Use `ipconfig` (Windows) or `ifconfig` (Linux) to get more information about your computers network configuration determine your network interface ip-address.

**My device does not wake up. Nothing happens!**  
You may select the IPv4-address of your computers network interface. Your sleeping device must be in the same network as your network interface.

## Roadmap (things to come in the future)
- Scan for network devices.
- See current status (power on or off) of devices.

## Further reading
[Usage of "wakeonlan" Python module](https://pypi.org/project/wakeonlan/)  
[WakeOnLAN protocoll on Wikipedia](http://en.wikipedia.org/wiki/Wake-on-LAN)  
[Tkinter Tutorials on pythontutorial.net](https://www.pythontutorial.net/tkinter/)  
