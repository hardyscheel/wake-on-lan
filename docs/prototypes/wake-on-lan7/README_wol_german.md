# WakeOnLAN

Nutzung als importierbares Modul, über die Konsole oder eigentständiges Skript möglich. Die Funktionen `send_magic_packet` und `wake_up` können in anderen Skripten importiert oder direkt über die Konsole aufgerufen werden.

---

### **Erläuterungen Quelltext:**

1. **`argparse`-Modul**:
   - Das Modul `argparse` wird verwendet, um Befehlszeilenargumente zu verarbeiten. Dies ermöglicht die Verwendung des Skripts über die Konsole.

2. **Hauptfunktion `main`**:
   - Die Funktion `main` wird nur ausgeführt, wenn das Skript direkt aufgerufen wird (`if __name__ == "__main__":`).
   - Sie liest die Befehlszeilenargumente ein und ruft die Funktion `wake_up` auf.

3. **Modulare Verwendung**:
   - Die Funktionen `create_magic_packet`, `send_magic_packet` und `wake_up` können in anderen Skripten importiert werden, z. B.:
     ```python
     from wol import wake_up
     wake_up("00:11:22:33:44:55", broadcast_ip="192.168.1.255")
     ```

---

### **Verwendung über die Konsole:**

**Aufruf über die Konsole**:
   - Beispiel 1: Einfacher Aufruf mit MAC-Adresse:
     ```bash
     python wol.py 00:11:22:33:44:55
     ```
   - Beispiel 2: Mit spezifischer Broadcast-IP und Interface-IP:
     ```bash
     python wol.py 00:11:22:33:44:55 --broadcast_ip 192.168.1.255 --interface_ip 192.168.1.100
     ```
