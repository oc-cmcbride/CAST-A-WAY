#include <HardwareSerial.h>

// Baud rate
#define BAUD 115200

// Socket rotation motor pins
#define ROT_DIR_PIN 2
#define ROT_STEP_PIN 3
// Camera/Laser translation motor pins
#define TRANS_DIR_PIN 4
#define TRANS_STEP_PIN 5
// Motor position sensors
#define ROT_SENSOR 11
#define TRANS_SENSOR_TOP_LIMIT 12
#define TRANS_SENSOR_BOT_LIMIT 13

// Step delay (in microseconds)
// #define STEP_DELAY_US 1000
#define STEP_DELAY_US 500

// Total number of repeatable actions
#define NUM_REPEATABLE_ACTIONS 4
// List of actions that can be repeated 
const char repeatableActions[] = {'r', 'R', 't', 'T'};
// Counters for repeated actions (-1 means repeate infinitely)
int actionCounters[] = {0, 0, 0, 0};

// Indices of actions in the above action arrays
#define ACTION_r 0
#define ACTION_R 1
#define ACTION_t 2
#define ACTION_T 3



void setup() {
  // Initialize serial connection
  Serial.begin(BAUD);

  // Declare input pins
  pinMode(ROT_SENSOR, INPUT);
  pinMode(TRANS_SENSOR_BOT_LIMIT, INPUT);
  pinMode(TRANS_SENSOR_TOP_LIMIT, INPUT);

  // Declare output pins
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
    executeCommand(command);
  }

  // Perform any repeated actions
  performRepeatedActions();

  // Check sensors to write data back to the computer
  checkSensors();
}

// Step a motor one time 
void step(int stepPin) {
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(STEP_DELAY_US);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(STEP_DELAY_US);
}

// Execute the specified command
void executeCommand(char command) {
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
      // Set and clear continuous actions
      case 'c':
        // Serial.write("Received continuous request...\n");
        command = 'c'; 
        while (command == 'c') {
          while (Serial.available() == 0);
          command = Serial.read();
        };
        for (int i = 0; i < NUM_REPEATABLE_ACTIONS; i++) {
          if (command == repeatableActions[i]) {
            makeRepeatedAction(i, -1);
            break;
          }
        }
        /*
        Serial.write("Continuous request set to: ");
        Serial.write(continuousAction);
        Serial.write('\n');
        */
        break;
      case 'C':
        for (int i = 0; i < NUM_REPEATABLE_ACTIONS; i++) {
          actionCounters[i] = 0;
        }
        break;
      default:
        // Serial.write("Unrecognized command: ");
        // Serial.write(command);
        // Serial.write("\n");
        break;
    }
}

// Make an action repeated
void makeRepeatedAction(int actionIndex, int reps) {
  // Verify a motor is not turning in multiple directions
  // Prioritize most recent repeat request
  switch (actionIndex) {
    // Rotational motor
    case ACTION_r:
      actionCounters[ACTION_R] = 0;
      break;
    case ACTION_R:
      actionCounters[ACTION_r] = 0;
      break;
    // Translational motor
    case ACTION_t:
      actionCounters[ACTION_T] = 0;
      break;
    case ACTION_T: 
      actionCounters[ACTION_t] = 0;
      break;
    default:
      break;
  }

  // Make action repeated 
  actionCounters[actionIndex] = reps;
}

// Perform repeated actions
void performRepeatedActions() {
  char action;
  for (int i = 0; i < NUM_REPEATABLE_ACTIONS; i++) {
    // Determine if action should be repeated 
    action = ' ';
    if (actionCounters[i] > 0) {
      action = repeatableActions[i];
      actionCounters[i]--;
    }
    else if (actionCounters[i] == -1) {
      action = repeatableActions[i];
    }

    // Perform action
    executeCommand(action);
  }
}

void checkSensors() {
  int readVal;
  
  // Check rotation motor sensor
  readVal = digitalRead(ROT_SENSOR);
  // Recall that the photointerrupter is set HIGH by default! 
  if (readVal == LOW && Serial.availableForWrite()) {
    Serial.write('1');
  }


  // Check translation motor sensors 
  readVal = digitalRead(TRANS_SENSOR_TOP_LIMIT);
  if (readVal == HIGH && Serial.availableForWrite()) {
    Serial.write('2');
  }

  readVal = digitalRead(TRANS_SENSOR_BOT_LIMIT);
  if (readVal == HIGH && Serial.availableForWrite()) {
    Serial.write('3');
  }
}
