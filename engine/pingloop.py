# engine/pingloop.py
import subprocess
import time
import platform
import requests
import re
from datetime import datetime
from engine.logforge import log_event
from engine.statuswatch import update_status
from engine.netheatmap import update_heatmap

PING_INTERVAL = 1  # seconds
HIGH_LATENCY_THRESHOLD = 250  # ms

def is_up_icmp(target):
    """Performs single ping and extracts latency in ms (cross-platform)."""
    try:
        if platform.system().lower() == "windows":
            output = subprocess.check_output(
                ["ping", "-n", "1", "-w", "1000", target],
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            match = re.search(r"time[=<]?\s*(\d+)\s*ms", output)
        else:
            output = subprocess.check_output(
                ["ping", "-c", "1", "-W", "1", target],
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            match = re.search(r"time[=<]?\s*(\d+(?:\.\d+)?)\s*ms", output)

        if match:
            latency = float(match.group(1))
            return True, latency
        return False, None
    except:
        return False, None

def is_up_http(target):
    """Performs basic HTTP GET request to verify web service availability."""
    try:
        r = requests.get(f"http://{target}", timeout=2)
        return r.status_code < 500
    except:
        return False

def calculate_threat_score(latency):
    """Returns threat score based on response delay."""
    if latency is None:
        return 100
    elif latency > HIGH_LATENCY_THRESHOLD:
        return 75
    elif latency > 150:
        return 40
    elif latency > 100:
        return 20
    return 0

def start_ping_cycle(target):
    """Main live ping + HTTP detection + threat engine loop."""
    print(f"[+] PINGLOOP STARTED FOR TARGET: {target}")
    previous_status = None
    downtime_start = None

    while True:
        # Dual verification: must respond to ping and HTTP
        status_icmp, latency = is_up_icmp(target)
        status_http = is_up_http(target)
        status = status_icmp and status_http

        now = datetime.now().strftime("%H:%M:%S")

        if status:
            if previous_status is False:
                recovered = f"[{now}] RECOVERY: {target} is back UP"
                log_event(recovered)
                print(recovered)
                downtime_start = None
            print(f"[{now}] STATUS: UP - Latency: {latency if latency else 'N/A'} ms")
        else:
            if previous_status is not False:
                downtime_start = datetime.now()
                downed = f"[{now}] ALERT: {target} is DOWN"
                log_event(downed)
                print(downed)
            else:
                delta = (datetime.now() - downtime_start).seconds
                print(f"[{now}] DOWN for {delta}s")

        # Update system-wide status memory + heatmap
        threat_score = calculate_threat_score(latency)
        update_status(status, latency, threat_score)
        update_heatmap()

        previous_status = status
        time.sleep(PING_INTERVAL)
