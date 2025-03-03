from wakeonlan import send_magic_packet

# Specify your network interface if you have more than one LAN interface. Especially if you have VMware, Hyper-V, WiFi, ...
# The magic packet will be routed through this interface.
send_magic_packet('fc.3f.db.0b.5c.bb', interface='192.168.200.35')  # WORKS!