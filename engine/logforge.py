# engine/logforge.py
import os
from datetime import datetime

LOG_DIR = "./logs"
LOG_FILE = None

def init_logging(target):
    global LOG_FILE
    os.makedirs(LOG_DIR, exist_ok=True)
    LOG_FILE = f"{LOG_DIR}/dead_signal_log_{target.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.log"
    with open(LOG_FILE, 'a', encoding='utf-8') as log:
        log.write(f"\n\n--- LOG START [{target}] @ {datetime.now()} ---\n")

def log_event(entry):
    with open(LOG_FILE, 'a', encoding='utf-8') as log:
        log.write(f"[{datetime.now().strftime('%H:%M:%S')}] {entry}\n")
