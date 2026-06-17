/*
  GyroGameController
  ==============================================

  Controls:
    Tilt Left        → Left Arrow
    Tilt Right       → Right Arrow
    Tilt Forward     → Down Arrow (Slide)
    Tilt Backward    → Up Arrow   (Jump)

*/

#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

// ─────────────────────────────────────────────
// Roll Hysteresis Config
// ─────────────────────────────────────────────

const int ROLL_RIGHT_ENTER = 20;
const int ROLL_RIGHT_EXIT  = 8;

const int ROLL_LEFT_ENTER  = -20;
const int ROLL_LEFT_EXIT   = -8;

// ─────────────────────────────────────────────
// Pitch Config
// ─────────────────────────────────────────────

const int PITCH_THRESHOLD = 20;
const int PITCH_DEADZONE  = 8;

// ─────────────────────────────────────────────
// Debounce
// ─────────────────────────────────────────────

const int TILT_DEBOUNCE_MS = 200;

unsigned long lastTiltSend = 0;
String lastTiltState = "CENTER";


// ─────────────────────────────────────────────

void setup() {

  Serial.begin(115200);
  Wire.begin();

  mpu.initialize();

  if (!mpu.testConnection()) {
    Serial.println("ERROR:MPU6050_NOT_FOUND");

    while (1);
  }

  Serial.println("STATUS:CALIBRATING");

  delay(2000);

  Serial.println("STATUS:READY");
}

// ─────────────────────────────────────────────

void loop() {

  handleGyro();

}


// ─────────────────────────────────────────────
// GYRO CONTROL
// ─────────────────────────────────────────────

void handleGyro() {

  int16_t ax, ay, az, gx, gy, gz;

  mpu.getMotion6(
    &ax,
    &ay,
    &az,
    &gx,
    &gy,
    &gz
  );

  float roll =
    atan2((float)ay, (float)az) *
    180.0 / PI;

  float pitch =
    atan2((float)ax, (float)az) *
    180.0 / PI;

  String tiltState = lastTiltState;

  // =====================================
  // PITCH HAS PRIORITY
  // =====================================

  if (pitch > PITCH_THRESHOLD) {

    tiltState = "FORWARD";
  }

  else if (pitch < -PITCH_THRESHOLD) {

    tiltState = "BACKWARD";
  }

  else {

    // =====================================
    // CENTER STATE
    // =====================================

    if (lastTiltState == "CENTER") {

      if (roll > ROLL_RIGHT_ENTER) {

        tiltState = "LEFT";
      }

      else if (roll < ROLL_LEFT_ENTER) {

        tiltState = "RIGHT";
      }
    }

    // =====================================
    // RIGHT STATE
    // =====================================

    else if (lastTiltState == "RIGHT") {

      if (roll < ROLL_RIGHT_EXIT) {

        tiltState = "CENTER";
      }

      else {

        tiltState = "RIGHT";
      }
    }

    // =====================================
    // LEFT STATE
    // =====================================

    else if (lastTiltState == "LEFT") {

      if (roll > ROLL_LEFT_EXIT) {

        tiltState = "CENTER";
      }

      else {

        tiltState = "LEFT";
      }
    }

    // =====================================
    // FORWARD/BACKWARD RETURN
    // =====================================

    else if (
      lastTiltState == "FORWARD" ||
      lastTiltState == "BACKWARD"
    ) {

      if (abs(pitch) < PITCH_DEADZONE) {

        tiltState = "CENTER";
      }
    }
  }

  unsigned long now = millis();

  if (
    tiltState != lastTiltState &&
    (now - lastTiltSend) > TILT_DEBOUNCE_MS
  ) {

    Serial.print("TILT:");
    Serial.println(tiltState);

    lastTiltState = tiltState;
    lastTiltSend  = now;
  }
}

