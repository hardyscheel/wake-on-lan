# WakeOnLAN
Wake up network devices in your LAN with Wake-on-LAN.

[README-images-01]: /docs/img/screenshot_main_window.png "Screenshot of the main window"
![README-images-01][README-images-01]

## Description
The Wake-on-LAN app is broadcasting Wake-on-LAN frames to wake up sleeping devices. Standard broadcast ip is 255.255.255.255 on port 9. You can manage manage and store several mac addresses. Your computers network interfaces can be listed from where you can choose the right one you want to send Wake-on-LAN frames from.
The app uses the wakeonlan Python module, a tkinter GUI and the psutil module to choose a network interface on your computer.

## Requirements to run the app
    pip install wakeonlan
    pip install psutil

## How to use the app
1. Add one or more destination MAC-addresses of your devices you want to wake up. You can also add names for them and edit or delete them later.
2. Select a MAC-address/device from the table.
3. (Optional) Select a network interface of your computer. Your sleeping device must be in the same network as your network interface.

The format of the MAC-addresses you can use must be in one of the following format:
- ff.ff.ff.ff.ff.ff
- 00-00-00-00-00-00
- FFFFFFFFFFFF

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
