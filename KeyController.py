"""
Subway Surfers Physical Controller — PC Side
=============================================
Reads serial messages from Arduino and maps them to keyboard inputs.

Requirements:
    pip install pyserial pynput

Usage:
    python subway_surfers_pc.py              # auto-detect port
    python subway_surfers_pc.py COM3         # Windows
    python subway_surfers_pc.py /dev/ttyUSB0 # Linux/Mac

Mappings:
    TILT:LEFT     →  Left Arrow  (change lane left)
    TILT:RIGHT    →  Right Arrow (change lane right)
    MUSCLE:FLEX   →  Up Arrow    (jump)
    MUSCLE:LONG   →  Down Arrow  (slide)
    MUSCLE:DOUBLE →  Space       (hoverboard)
"""

import sys
import time
import serial
import serial.tools.list_ports
from pynput.keyboard import Key, Controller

keyboard = Controller()

# ── Key Mappings ─────────────────────────────────────────────────
ACTION_MAP = {
    "TILT:LEFT":     Key.left,
    "TILT:RIGHT":    Key.right,
    "MUSCLE:FLEX":   Key.up,       # jump
    "MUSCLE:LONG":   Key.down,     # slide
    "MUSCLE:DOUBLE": Key.space,    # hoverboard
}

# How long to hold each key (seconds)
KEY_HOLD = {
    Key.left:  0.08,
    Key.right: 0.08,
    Key.up:    0.08,
    Key.down:  0.05,
    Key.space: 0.08,
}

# ── Serial Port Detection ─────────────────────────────────────────
def find_arduino_port():
    """Auto-detect the first Arduino-like serial port."""
    ports = serial.tools.list_ports.comports()
    for p in ports:
        desc = (p.description or "").lower()
        if any(k in desc for k in ("arduino", "ch340", "cp210", "ftdi", "usb serial")):
            return p.device
    # Fallback — return first available port
    if ports:
        return ports[0].device
    return None


def send_key(key):
    """Press and release a key with a short hold."""
    hold = KEY_HOLD.get(key, 0.08)
    keyboard.press(key)
    time.sleep(hold)
    keyboard.release(key)


# ── Label helpers ─────────────────────────────────────────────────
KEY_LABELS = {
    Key.left:  "← LEFT",
    Key.right: "→ RIGHT",
    Key.up:    "↑ JUMP",
    Key.down:  "↓ SLIDE",
    Key.space: "⬛ HOVERBOARD",
}


# ── Main Loop ─────────────────────────────────────────────────────
def main():
    port = sys.argv[1] if len(sys.argv) > 1 else find_arduino_port()

    if not port:
        print("❌  No Arduino found. Plug it in or pass port as argument.")
        sys.exit(1)

    print(f"🎮  Subway Surfers Controller")
    print(f"📡  Connecting to {port} @ 115200 baud …")

    try:
        ser = serial.Serial(port, 115200, timeout=1)
    except serial.SerialException as e:
        print(f"❌  Could not open port: {e}")
        sys.exit(1)

    time.sleep(2)   # Wait for Arduino to reset after opening port
    print("✅  Connected! Focus the Subway Surfers window and start playing.\n")
    print(f"   {'SENSOR EVENT':<20} → ACTION")
    print(f"   {'-'*40}")

    # Tilt state tracking — only trigger on transition to avoid key spam
    last_tilt = "CENTER"

    try:
        while True:
            raw = ser.readline()
            if not raw:
                continue

            line = raw.decode("utf-8", errors="ignore").strip()

            if not line:
                continue

            # Status / debug messages from Arduino
            if line.startswith("STATUS:") or line.startswith("ERROR:"):
                print(f"   [Arduino] {line}")
                continue

            # Tilt events — only send on change, ignore TILT:CENTER
            if line.startswith("TILT:"):
                direction = line.split(":")[1]
                if direction == "CENTER":
                    last_tilt = "CENTER"
                    continue
                if direction != last_tilt:
                    key = ACTION_MAP.get(line)
                    if key:
                        label = KEY_LABELS.get(key, str(key))
                        print(f"   {line:<20} → {label}")
                        send_key(key)
                    last_tilt = direction
                continue

            # Muscle events
            if line.startswith("MUSCLE:"):
                key = ACTION_MAP.get(line)
                if key:
                    label = KEY_LABELS.get(key, str(key))
                    print(f"   {line:<20} → {label}")
                    send_key(key)
                continue

    except KeyboardInterrupt:
        print("\n👋  Controller stopped.")
    finally:
        ser.close()


if __name__ == "__main__":
    main()
