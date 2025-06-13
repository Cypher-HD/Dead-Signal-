# engine/reportgen.py
import json
import os
from datetime import datetime
from engine.statuswatch import get_status_summary
from engine.logforge import LOG_FILE

def generate_report(target):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    out_dir = "./reports"
    os.makedirs(out_dir, exist_ok=True)

    # Load logs
    with open(LOG_FILE, 'r') as f:
        log_content = f.readlines()

    status = get_status_summary()

    # Construct Report Structure
    report = {
        "target": target,
        "timestamp": timestamp,
        "last_status": status.get("last_status"),
        "last_latency": status.get("last_latency"),
        "threat_score": status.get("threat_score"),
        "log": log_content
    }

    # Save JSON
    json_path = os.path.join(out_dir, f"report_{target.replace('.', '_')}_{timestamp}.json")
    with open(json_path, 'w') as jf:
        json.dump(report, jf, indent=4)

    # Save Human-Readable TXT
    txt_path = os.path.join(out_dir, f"report_{target.replace('.', '_')}_{timestamp}.txt")
    with open(txt_path, 'w') as tf:
        tf.write(f"=== DEAD SIGNAL REPORT ===\n")
        tf.write(f"Target: {target}\nGenerated: {timestamp}\n\n")
        tf.write(f"Last Known Status: {'UP' if status.get('last_status') else 'DOWN'}\n")
        tf.write(f"Last Latency: {status.get('last_latency')} ms\n")
        tf.write(f"Threat Score: {status.get('threat_score')}/100\n\n")
        tf.write("---- LOGS ----\n")
        tf.writelines(log_content)

    print(f"\n[+] Report Generated:\n- {json_path}\n- {txt_path}")
