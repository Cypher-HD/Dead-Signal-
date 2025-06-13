# engine/trafficwatch.py
import time
import random
from datetime import datetime
from engine.logforge import log_event

def simulate_traffic_probe(target):
    """
    Simulates traffic estimation using pseudo-random logic.
    Replace with raw socket capture or PCAP-based analyzer in full deployment.
    """
    # Simulated ranges based on probabilistic TTL/ACK/SYN patterns
    base = random.randint(10, 30)  # base traffic pattern
    spike_chance = random.randint(1, 10)

    if spike_chance == 10:
        return base + random.randint(100, 300)  # simulate spike
    elif spike_chance == 1:
        return 0  # simulate blackout
    return base + random.randint(0, 20)

def start_traffic_watch(target):
    print(f"\n[+] TRAFFICWATCH ENGAGED :: Monitoring traffic to {target}")
    log_event(f"Traffic watch started on target: {target}")

    while True:
        pps = simulate_traffic_probe(target)
        now = datetime.now().strftime("%H:%M:%S")

        if pps > 200:
            alert = f"[{now}] ⚠ HIGH TRAFFIC: {pps} PPS detected to {target}"
            print(alert)
            log_event(alert)
        elif pps == 0:
            alert = f"[{now}] ⚠ NO TRAFFIC: Potential blackout on {target}"
            print(alert)
            log_event(alert)
        else:
            print(f"[{now}] Traffic: {pps} PPS")

        time.sleep(1)


current_pps = 0


def get_current_pps():
    return current_pps


def simulate_traffic_probe(target):
    global current_pps
    base = random.randint(10, 30)
    spike_chance = random.randint(1, 10)

    if spike_chance == 10:
        current_pps = base + random.randint(100, 300)
    elif spike_chance == 1:
        current_pps = 0
    else:
        current_pps = base + random.randint(0, 20)

    return current_pps
