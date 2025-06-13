# engine/portscan.py
import socket
import threading
from datetime import datetime
from engine.logforge import log_event

open_ports = []

def scan_port(target, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect((target, port))
        s.close()
        open_ports.append(port)
        log_event(f"[PORT OPEN] {target}:{port}")
    except:
        pass

def start_portscan(target, ports=None):
    print(f"[+] PORT SCAN STARTED on {target}")
    log_event(f"[PORTSCAN] Target: {target}")

    if not ports:
        ports = list(range(20, 1024))  # Default: top 1K TCP

    threads = []

    for port in ports:
        t = threading.Thread(target=scan_port, args=(target, port))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f"[+] Scan Complete: {len(open_ports)} open ports")
    log_event(f"[PORTSCAN COMPLETE] Open ports: {open_ports}")

def get_open_ports():
    return open_ports
