#include <HardwareSerial.h>

// Socket rotation motor pins
#define ROT_DIR_PIN 2
#define ROT_STEP_PIN 3
// Camera/Laser translation motor pins
#define TRANS_DIR_PIN 4
#define TRANS_STEP_PIN 5

// Step delay (in microseconds)
#define STEP_DELAY_US 1000


void setup() {
  // Initialize serial connection
  Serial.begin(9600);

  // Declare pins as output 
  pinMode(ROT_DIR_PIN, OUTPUT);
  pinMode(ROT_STEP_PIN, OUTPUT);
  pinMode(TRANS_DIR_PIN, OUTPUT);
  pinMode(TRANS_STEP_PIN, OUTPUT);

  // Set the initial spin directions 
  // HIGH = CW/CCW??, LOW = CW/CCW???
  digitalWrite(ROT_DIR_PIN, HIGH);
  digitalWrite(TRANS_DIR_PIN, HIGH);
}

void loop() {
  // Listen to serial connection 
  if (Serial.available() > 0) {
    // Read received character 
    char command = Serial.read();

    // Perform action based on character 
    switch (command) {
      // Step translation motor
      case 't':
        digitalWrite(TRANS_DIR_PIN, HIGH);
        step(TRANS_STEP_PIN);
        break;
      case 'T':
        digitalWrite(TRANS_DIR_PIN, LOW);
        step(TRANS_STEP_PIN);
        break;
      // Step rotation motor
      case 'r':
        digitalWrite(ROT_DIR_PIN, HIGH);
        step(ROT_STEP_PIN);
        break;
      case 'R':
        digitalWrite(ROT_DIR_PIN, LOW);
        step(ROT_STEP_PIN);
        break;
      default:
        break;
    }
  }

  // Check sensors to write data back to the computer
  // TODO: Write sensor code 
  // Use Serial.write() to write data back to the computer 
}

void step(int stepPin) {
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(STEP_DELAY_US);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(STEP_DELAY_US);
}
