#include <HardwareSerial.h>

// Socket rotation motor pins
#define rotDirPin 2
#define rotStepPin 3
// Camera/Laser translation motor pins
#define transDirPin 4
#define transStepPin 5

// Step delay (in microseconds)
#define STEP_DELAY_US 500

void setup() {
  // Initialize serial connection
  Serial.begin(9600);

  // Declare pins as output 
  pinMode(rotDirPin, OUTPUT);
  pinMode(rotStepPin, OUTPUT);
  pinMode(transDirPin, OUTPUT);
  pinMode(transStepPin, OUTPUT);

  // Set the initial spin directions 
  // HIGH = CW/CCW??, LOW = CW/CCW???
  digitalWrite(rotDirPin, HIGH);
  digitalWrite(transDirPin, HIGH);
}

void loop() {
  // Listen to serial connection 
  if (Serial.available() > 0) {
    // Read received character 
    char command = Serial.read();

    // Perform action based on character 
    if (command == 't') {
      // Step translation motor 
      step(transStepPin);
    }
    else if (command == 'r') {
      // Step rotation motor 
      step(rotStepPin);
    }
  }
}

void step(int stepPin) {
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(STEP_DELAY_US);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(STEP_DELAY_US);
}
