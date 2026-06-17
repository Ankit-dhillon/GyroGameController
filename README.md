# GyroGameController

GyroGameController is a real-time motion-based gaming controller that uses an **Arduino + MPU6050 gyroscope + Python PC interface** to convert physical tilt movements into keyboard inputs for PC games.

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


GyroGameController/
│
├── GyroController.ino # Arduino firmware for MPU6050
├── gyro_game_pc.py # Python PC-side controller
├── README.md


---

## 🧰 Requirements

### 1. Install Python
Download Python 3.x:  
https://www.python.org/downloads/

### 2. Install Arduino IDE  
https://www.arduino.cc/en/software

### 3. Install Python Dependencies
```bash
pip install pyserial pynput
⚙️ Setup Instructions
1. Upload Arduino Code
Open GyroController.ino in Arduino IDE
Select board (Arduino Uno / Nano)
Select correct COM port
Upload firmware to the board
2. Clone / Download Repository
git clone https://github.com/YOUR_USERNAME/GyroGameController.git
cd GyroGameController
3. Run the Python Controller
python gyro_game_pc.py

Or specify port manually:

python gyro_game_pc.py COM3
🎮 Controls
Gesture	Action
Tilt Left	Move Left
Tilt Right	Move Right
Tilt Forward	Jump
Tilt Backward	Slide
🧠 System Architecture
MPU6050 Sensor
      ↓
Arduino Board (Motion Processing)
      ↓ Serial Communication
Python Controller Script
      ↓
Keyboard Simulation (Arrow Keys)
      ↓
Game Input Control
🧩 Applications
Motion-based gaming controllers
Human–computer interaction (HCI)
Embedded systems projects
IoT and sensor integration learning
Hackathon / internship demonstrations
Assistive gaming systems
