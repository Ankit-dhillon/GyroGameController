# GyroGameController

GyroGameController is a real-time motion-based gaming controller that uses an Arduino + MPU6050 gyroscope + Python PC interface to convert physical tilt movements into keyboard inputs for PC games.

---

## Features

- Detects and connects to Arduino-based gyro devices.
- Streams real-time motion (tilt) data via serial communication.
- Converts motion gestures into keyboard inputs.
- Low-latency response for gaming applications.
- Stable tilt detection with anti-spam filtering.
- Cross-platform support (Windows / Linux / Mac).

---

## 📁 Project Folder Structure
```plain text
GyroGameController/
│
├── GyroController.ino # Arduino firmware for MPU6050
├── gyro_game_pc.py # Python PC-side controller
└── README.md
```


---

## Requirements

### 1. Install Python
Download Python 3.x  
https://www.python.org/downloads/

### 2. Install Arduino IDE  
https://www.arduino.cc/en/software

### 3. Install Python Dependencies
    `pip install pyserial pynput`

## Setup Instructions
### 1. Upload Arduino Code 
    `https://github.com/Ankit-dhillon/GyroGameController/blob/main/GyroController.ino`


### 2. Download the repository `GyroGameConroller`
    - GyroGameController from github - `https://github.com/Ankit-dhillon/GyroGameController.git`

### 3. Run the Python Controller
    `python KeyController.py`

## Controls  
```plain text
| Gesture       | Action     |
| ------------- | ---------- |
| Tilt Left     | Move Left  |
| Tilt Right    | Move Right |
| Tilt Forward  | Jump       |
| Tilt Backward | Slide      |
```


## Applications
- Motion-based gaming controllers
- Human–computer interaction (HCI)
- Embedded systems projects
- IoT and sensor integration learning
- Hackathons and project demonstrations
- Assistive gaming systems

