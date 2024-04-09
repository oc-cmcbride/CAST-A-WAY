"""
Morgan Demuth
Feb 28, 2024
Systems Engineering Design
Team CAST-A-WAY

This program serially communication with the Arduino Mega to control motor movements and receive data.
"""
import time
import serial
ser = serial.Serial('COM3', 115200)
repT = 10000
repR = 20
charD = 't'
charU = 'T'
charR = 'R'
charL = 'r'


class Driver:
    def __init__(self):
        self.position = [0, 0]  # [rot, trans]
        self.update_position_rot = 2  # degrees
        self.update_position_trans = 1  # inches
        self.character = 'T'
        self.repetitions = 50
        self.top_button = False
        self.bottom_button = False
        self.rot_sensor = False

    def move_to_start(self):
        print('Moving to start')
        above = True
        while not self.bottom_button:
            self.translate_down()
            self.check_sensors()

    def rotate_left(self):
        ser.write((charL * repR).encode())
        time.sleep(1)
        print('lefting')
        # step motor left
        self.position[0] -= self.update_position_rot

    def rotate_right(self):
        ser.write((charR * repR).encode())
        time.sleep(1)
        print('righting')
        # step motor right
        # wait update position
        self.position[0] += self.update_position_rot

    def translate_up(self):
        ser.write((charU * repT).encode())
        time.sleep(1)
        print('Moving Up')
        # step up one ??
        self.position[1] -= self.update_position_trans

    def translate_down(self):
        ser.write((charD * repT).encode())
        time.sleep(1)
        print('downing')
        # step down one ??
        self.position[1] += self.update_position_trans

    def reset(self):
        # back to top
        count = 0
        while count != 2:
            self.translate_up()
            self.check_sensors()
            count += 1

        # back to center
        count = 0
        while count != 2:
            self.rotate_left()
            self.check_sensors()
            count += 1

        self.position = [0, 0]
        print('reset')
        return True

    def check_sensors(self):
        self.top_button = False
        self.bottom_button = False
        self.rot_sensor = False
        # serial read into this
        while ser.in_waiting > 0:
            read_data = ser.readline().strip().decode()
            if '1' in read_data:
                self.rot_sensor = True
            if '2' in read_data:
                self.top_button = True
            if '3' in read_data:
                self.bottom_button = True

    def check_scan_complete(self):
        print('idk how we do this')
        return False
