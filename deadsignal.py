# deadsignal.py
import os
import time
import threading
from engine.cliux import display_banner
from engine.pingloop import start_ping_cycle
from engine.trafficwatch import start_traffic_watch
from engine.reconcore import perform_recon
from engine.statuswatch import monitor_status
from engine.logforge import init_logging
from engine.portscan import start_portscan
from engine.keypress import listen_for_keys
from engine.livehud import run_live_display

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    clear_screen()
    display_banner()

    print("\n[+] DEAD SIGNAL ENGAGED")
    target = input("[?] Enter domain or IP to analyze: ").strip()

    if not target:
        print("[!] No target entered. Aborting.")
        exit()

    # Initialize log
    init_logging(target)

    # Recon pass
    print("[*] Running passive recon...\n")
    perform_recon(target)

    # Port scan (non-blocking)
    print("[*] Starting port scan...\n")
    threading.Thread(target=start_portscan, args=(target,), daemon=True).start()

    # Launch background threads
    threading.Thread(target=start_ping_cycle, args=(target,), daemon=True).start()
    threading.Thread(target=start_traffic_watch, args=(target,), daemon=True).start()
    threading.Thread(target=monitor_status, daemon=True).start()
    threading.Thread(target=listen_for_keys, args=(target,), daemon=True).start()

    # Lock CLI to live HUD
    run_live_display(target)

if __name__ == "__main__":
    main()
