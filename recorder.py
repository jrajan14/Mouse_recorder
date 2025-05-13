import json
import time
import pyautogui
import keyboard  # New import for key detection
from pynput import mouse
import sys
from protocol import MouseData
import socket
import numpy as np

ADDRESS = ('localhost', 12345)  # UDP address for sending data
WIDTH = 3840
HEIGHT = 2160

def send_udp(points: MouseData):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(points.pack(), ADDRESS)

# Configuration
RECORDING_DELAY = 3  # seconds
OUTPUT_FILE = "mouse_track.json"
MIN_MOVE_INTERVAL = 0.01  # Minimum time between move events (seconds)
STOP_HOTKEY = 'scroll lock'  # Change this to your preferred key
# Alternative options:
# 'ctrl+m' for Ctrl+M combination
# 'pause' for Pause/Break key
# 'insert' for Insert key

# Data storage
events = []
start_time = None
mouse_pressed = False
last_move_time = 0

def on_move(x, y):
    global last_move_time
    if start_time is None:
        return
    
    current_time = time.time()
    if current_time - last_move_time < MIN_MOVE_INTERVAL and mouse_pressed:
        return
    
    last_move_time = current_time
    timestamp = current_time - start_time
    events.append({
        "type": "move",
        "x": x,
        "y": y,
        "time": timestamp,
        "pressed": mouse_pressed
    })

    if mouse_pressed:
        send_udp(MouseData(np.array([[x/WIDTH, y/HEIGHT]])))  # Send the coordinates as a single point

def on_click(x, y, button, pressed):
    global mouse_pressed
    if start_time is None:
        return
    
    timestamp = time.time() - start_time
    mouse_pressed = pressed
    events.append({
        "type": "click",
        "x": x,
        "y": y,
        "button": str(button),
        "state": "pressed" if pressed else "released",
        "time": timestamp
    })

    if pressed:
        send_udp(MouseData(np.array([[x/WIDTH, y/HEIGHT]])))  # Send the coordinates as a single point


def on_scroll(x, y, dx, dy):
    if start_time is None:
        return
    
    timestamp = time.time() - start_time
    events.append({
        "type": "scroll",
        "x": x,
        "y": y,
        "dx": dx,
        "dy": dy,
        "time": timestamp
    })

# Continuously check for the stop key
def check_stop_key():
    if '+' in STOP_HOTKEY:
        # For combination keys like Ctrl+M
        keys = STOP_HOTKEY.split('+')
        return all(keyboard.is_pressed(key) for key in keys)
    else:
        # For single keys like Scroll Lock
        return keyboard.is_pressed(STOP_HOTKEY)

def main():
    global start_time
    print(f"Mouse recorder will start in {RECORDING_DELAY} seconds...")
    print(f"Press {STOP_HOTKEY.upper()} at any time to stop recording")
    time.sleep(RECORDING_DELAY)
    print("Recording started. You can also press Ctrl+C to stop.")
    
    start_time = time.time()
    listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    
    try:
        listener.start()
        while True:
            if check_stop_key():
                print("\nRecording stopped by hotkey.")
                break
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nRecording stopped by Ctrl+C.")
    finally:
        listener.stop()
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(events, f, indent=2)
    print(f"Recorded {len(events)} events saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()