# 🖱️ Mouse Recorder & Player with UDP Streaming

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

```bash
.
├── recorder.py       # Record mouse events and send UDP data
├── player.py         # Replay recorded mouse events
├── mouse_track.json  # Output file from recorder
├── protocol.py       # Defines TouchData for UDP packet structure
├── protocol.py       # To receive UDP messages sent via protocol.py
└── README.md         # Project documentation


🖥️ Requirements
Python 3.7+
pyautogui
pynput
keyboard
numpy


```bash


