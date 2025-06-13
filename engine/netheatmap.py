# engine/netheatmap.py
from datetime import datetime
from engine.statuswatch import get_status_summary

HEAT_TILES = {
    "green": "🟩",
    "yellow": "🟨",
    "red": "🟥",
    "black": "⬛"
}

history = []

def classify_tile(latency):
    if latency is None:
        return HEAT_TILES["black"]
    elif latency < 100:
        return HEAT_TILES["green"]
    elif latency < 200:
        return HEAT_TILES["yellow"]
    elif latency >= 200:
        return HEAT_TILES["red"]

def update_heatmap():
    status = get_status_summary()
    tile = classify_tile(status.get("last_latency"))
    history.append(tile)

    if len(history) > 40:
        history.pop(0)

    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] NETWORK HEATMAP")
    print("".join(history))
def get_heatmap_visual():
    return "".join(history)
