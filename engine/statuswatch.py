# engine/statuswatch.py
import time
from datetime import datetime

# Global status cache
last_latency = None
last_status = None
last_score = None

def update_status(status, latency, threat_score):
    """Update the current status snapshot"""
    global last_latency, last_status, last_score
    last_latency = latency
    last_status = status
    last_score = threat_score

def get_status_summary():
    """Return current memory-cached status dict"""
    return {
        "last_status": last_status,
        "last_latency": last_latency,
        "threat_score": last_score
    }

def monitor_status():
    """Periodic summary display function (runs in background if desired)"""
    while True:
        summary = get_status_summary()
        now = datetime.now().strftime("%H:%M:%S")
        if summary["last_status"] is not None:
            status_str = "UP" if summary["last_status"] else "DOWN"
            print(f"[{now}] STATUS WATCH: {status_str} | Latency: {summary['last_latency']} ms | Threat Score: {summary['threat_score']}/100")
        else:
            print(f"[{now}] STATUS WATCH: No status yet.")
        time.sleep(10)
