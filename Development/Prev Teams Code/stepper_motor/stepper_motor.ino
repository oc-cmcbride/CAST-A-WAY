#include <HardwareSerial.h>

// Define stepper motor connections:
#define dirPin 2
#define stepPin 3


void setup() {
  // Initialize serial connection
  Serial.begin(9600);

  // Declare pins as output:
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);

  // Set the spinning direction CW/CCW:
  digitalWrite(dirPin, HIGH);


}

void loop() {
  /*
  for (int i = 0; i<200; i++) {
    step();
    delay(300);
  }
  */

// this is to read a message from Noah's code that tells the motor to take 1 step
  if(Serial.available() > 0) {
    char command = Serial.read();
    if(command == 's') {
      step();
      Serial.write("done\n");
    }
  }
}

void step() {
  // These lines result in 1 step:
  digitalWrite(stepPin, HIGH);
  digitalWrite(stepPin, LOW);
}
