import json
import time
import pyautogui
import keyboard
from pynput.mouse import Button
import sys

# Configuration
INPUT_FILE = "mouse_track.json"
SPEED_FACTOR = 1.0
MIN_DELAY = 0.001  # 1ms minimum delay
DRAG_PREDICTION = True  # Enable predictive dragging for smoother curves
STOP_KEY = 'scroll lock'  # For emergency stop

def convert_button(button_str):
    if "Button.left" in button_str:
        return "left"
    elif "Button.right" in button_str:
        return "right"
    elif "Button.middle" in button_str:
        return "middle"
    return "left"

def check_stop_key():
    return keyboard.is_pressed(STOP_KEY)

def main():
    try:
        with open(INPUT_FILE, "r") as f:
            events = json.load(f)
    except FileNotFoundError:
        print(f"Error: File {INPUT_FILE} not found.")
        return
    
    if not events:
        print("No events to replay.")
        return
    
    print(f"Loaded {len(events)} events. Starting playback in 3 seconds...")
    print(f"Press {STOP_KEY.upper()} at any time to stop playback")
    time.sleep(3)
    
    start_time = time.time()
    current_button = None
    last_position = pyautogui.position()
    
    for i, event in enumerate(events):
        # Check for emergency stop before each event
        if check_stop_key():
            print("\nEMERGENCY STOP: Playback terminated by user")
            sys.exit(0)
        
        target_time = event["time"] / SPEED_FACTOR
        elapsed = time.time() - start_time
        remaining_wait = target_time - elapsed
        
        if remaining_wait > 0:
            # Check for stop key during wait period
            sleep_interval = 0.05  # Check every 50ms
            while remaining_wait > 0:
                if check_stop_key():
                    print("\nEMERGENCY STOP: Playback terminated by user")
                    sys.exit(0)
                actual_sleep = min(sleep_interval, remaining_wait)
                time.sleep(actual_sleep)
                remaining_wait -= actual_sleep
        
        try:
            if event["type"] == "move":
                x, y = event["x"], event["y"]
                
                if DRAG_PREDICTION and current_button and i < len(events) - 1:
                    next_event = events[i + 1]
                    if next_event["type"] == "move":
                        pyautogui.dragTo(x, y, button=current_button, duration=0.0001, _pause=False)
                    else:
                        pyautogui.dragTo(x, y, button=current_button, _pause=False)
                elif event.get("pressed", False) and current_button:
                    pyautogui.dragTo(x, y, button=current_button, _pause=False)
                else:
                    pyautogui.moveTo(x, y, _pause=False)
                
                last_position = (x, y)
                
            elif event["type"] == "click":
                button = convert_button(event["button"])
                if event["state"] == "pressed":
                    pyautogui.mouseDown(x=event["x"], y=event["y"], button=button, _pause=False)
                    current_button = button
                else:
                    pyautogui.mouseUp(x=event["x"], y=event["y"], button=button, _pause=False)
                    current_button = None
                    
            elif event["type"] == "scroll":
                pyautogui.scroll(int(event["dy"] * 10), x=event["x"], y=event["y"], _pause=False)
                
        except Exception as e:
            print(f"Error executing event {i}: {e}")
            continue
    
    print("Playback complete.")

if __name__ == "__main__":
    try:
        # Install keyboard package if not already installed
        try:
            import keyboard
        except ImportError:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "keyboard"])
            import keyboard
        
        main()
    except KeyboardInterrupt:
        print("\nPlayback stopped by user (Ctrl+C)")
    except Exception as e:
        print(f"Error: {e}")
