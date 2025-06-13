# engine/keypress.py
import keyboard
from engine import reportgen

def listen_for_keys(target):
    def handle_key(event):
        if event.name.lower() == 'r':
            print("\n[KEYPRESS] [R] detected. Generating report...\n")
            reportgen.generate_report(target)
        elif event.name.lower() == 'q':
            print("\n[KEYPRESS] [Q] detected. Exiting DEAD SIGNAL.")
            exit()

    keyboard.on_press(handle_key)
    keyboard.wait()  # Keeps listener alive
