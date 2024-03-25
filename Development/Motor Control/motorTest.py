'''
motorTest.py

Colin McBride
Mar 6, 2024
Systems Engineering Design
Team CAST-A-WAY

This file contains various tests for the motor subsystem. 
'''
import serial
import time

'''
CONSTANTS
'''
PORT = "COM3"
BAUD = 9600
NUM_STEPS = 10

def turnSingleDirection():
    print("Opening serial port... ", end="")
    ser = serial.Serial(port = PORT, baudrate = BAUD, timeout = 0.1)
    time.sleep(1)   # Short delay to give the serial port time to open 
    print("Serial port open")

    print("Testing rotational motor... ", end="")
    for i in range(NUM_STEPS):
        ser.write(bytes('r', 'utf-8'))
        time.sleep(0.5)
    print("Done")
    
    time.sleep(2)
    
    print("Testing translational motor... ", end="")
    for i in range(NUM_STEPS):
        ser.write(bytes('t', 'utf-8'))
        time.sleep(0.5)
    print("Done")

    print("Closing serial port... ", end="")
    ser.close()
    print("Done")
# end turnSingleDirection

def turnBothDirections():
    print("Opening serial port... ", end="")
    ser = serial.Serial(port = PORT, baudrate = BAUD, timeout = 0.1)
    time.sleep(1)   # Short delay to give the serial port time to open 
    print("Serial port open")

    print("Testing rotational motor... ", end="")
    print("Clockwise...", end="")
    for i in range(NUM_STEPS):
        ser.write(bytes('r', 'utf-8'))
        time.sleep(0.5)
    time.sleep(1)
    print("Counter-clockwise...", end="")
    for i in range(NUM_STEPS):
        ser.write(bytes('R', 'utf-8'))
        time.sleep(0.5)
    print("Done")
    
    time.sleep(2)
    
    print("Testing translational motor... ", end="")
    print("Clockwise...", end="")
    for i in range(NUM_STEPS):
        ser.write(bytes('t', 'utf-8'))
        time.sleep(0.5)
    time.sleep(1)
    print("Counter-clockwise...", end="")
    for i in range(NUM_STEPS):
        ser.write(bytes('T', 'utf-8'))
        time.sleep(0.5)
    print("Done")

    print("Closing serial port... ", end="")
    ser.close()
    print("Done")
# end turnBothDirections

def main():
    # turnSingleDirection()
    turnBothDirections()
# end main
    
if __name__ == "__main__":
    main()
