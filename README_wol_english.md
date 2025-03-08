# wol - WakeOnLAN

Can be used as an importable module, via the console or as a standalone script. The functions `send_magic_packet` and `wake_up` can be imported into other scripts or called directly via the console.

---

### **Explanations to the source code**

1. **`argparse` Module**:
   - The `argparse` module is used to handle command-line arguments, enabling the script to be used via the console.

2. **Main Function**:
   - The `main` function is executed only if the script is run directly (`if __name__ == "__main__":`).
   - It reads the command-line arguments and calls the `wake_up` function.

3. **Modular Usage**:
   - The functions `create_magic_packet`, `send_magic_packet`, and `wake_up` can be imported into other scripts, e.g.:
     ```python
     from wol import wake_up
     wake_up("00:11:22:33:44:55", broadcast_ip="192.168.1.255")
     ```

---

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
