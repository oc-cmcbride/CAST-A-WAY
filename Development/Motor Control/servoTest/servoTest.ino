#include <Servo.h>

#define SERVO_PIN 9
Servo myservo;
int pos = 0;

void setup() {
  // put your setup code here, to run once:
  myservo.attach(SERVO_PIN);
}

void loop() {
  int i;
  // Repeat program 4 times
  for (i = 0; i < 4; i++) {
    for (pos = 0; pos <= 180; pos += 45) {
      myservo.write(pos);
      delay(1000);
    }
    for (pos = 180; pos >= 0; pos -= 45) {
      myservo.write(pos);
      delay(1000);
    }
  }

  // Stay idle after servo test is done
  while (1);
}
