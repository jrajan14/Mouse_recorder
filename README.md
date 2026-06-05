# 🖱️ Mouse Recorder & Player with UDP Streaming.   
    
This project provides a Python-based mouse **recorder** and **player** that captures mouse events (movements, clicks, and scrolls), stores them in a JSON file, and streams real-time touch data over **UDP**. It is designed for **UI testing**, **automation**, and **input replay systems**.     

---     

## 📦 Features  
 
- ✅ **Mouse Event Recording** (movement, click, scroll)  
- 📤 **UDP Touch Data Streaming** (normalized coordinates) 
- ▶️ **Playback with Timing Accuracy**
- 🐍 **Smooth Drag Prediction**
- ⏱️ **Adjustable Playback Speed**
- 🛑 **Emergency Stop Key Support**
- 💾 **JSON Output for Analysis/Replay**

---

## 📁 Project Structure  

```
.
├── recorder.py       # Record mouse events and send UDP data
├── player.py         # Replay recorded mouse events
├── mouse_track.json  # Output file from recorder
├── protocol.py       # Defines TouchData for UDP packet structure
├── protocol.py       # To receive UDP messages sent via protocol.py
└── README.md         # Project documentation
```

## 🖥️ Requirements
- **Python 3.7+**
- **pyautogui**
- **pynput**
- **keyboard**
- **numpy**

```
pip install pyautogui pynput keyboard numpy
```
🚀 Usage
-🎙️ Record Mouse Events
```
python recorder.py
```
- Waits 3 seconds before starting.
- Records movements, clicks, scrolls.
- Sends live (x, y) over UDP if mouse is pressed.
- Press Scroll Lock or Ctrl+C to stop.
- Output saved to: ```mouse_track.json```

🎬 Play Back Events
``` python player.py ```
- Replays all recorded events.
- Uses original timing unless modified via SPEED_FACTOR.
- Supports drag prediction for smoother paths.
- Press Scroll Lock or ```Ctrl+C``` to stop at any time.

⚙️ Configuration Options
- You can customize in ```recorder.py``` and ```player.py```:

**Option Descriptions**
- ```RECORDING_DELAY```	Delay before starting recording
- ```SPEED_FACTOR```	Playback speed multiplier (e.g., 2.0 = 2x)
- ```STOP_KEY	Hotkey``` to stop recording/playback
- ```DRAG_PREDICTION```	Enable smoother drag motion
- ```ADDRESS	UDP``` target address and port
- ```WIDTH/HEIGHT```	Screen resolution for coordinate scaling

📡 UDP Streaming Format
- The TouchData class in ```protocol.py``` is used to:
- Normalize coordinates (0–1 range)
- Package them into byte format
- Send via UDP to a target listener

You can customize this class to match your target application's protocol.

🧪 Example Use Cases
- Automated UI testing for desktop apps
- Creating reproducible input demos
- Remote control/input replay in custom environments
- Input stream generation for touch emulation

🛠️ Future Improvements
- Add support for keyboard event capture
- Include GUI for easier recording/playback
- Cross-platform enhancements for hotkey handling

🙌 Acknowledgments
- Built using:
```
pyautogui
pynput
keyboard
```
