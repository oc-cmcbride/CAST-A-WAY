"""
Morgan Demuth
Feb 28, 2024
Systems Engineering Design
Team CAST-A-WAY

This program serially communication with the Arduino Mega to control motor movements and receive data.
"""


class Driver:
    def __init__(self):
        self.position = [0, 0]  # [rot, trans]
        self.update_position_rot = 2  # degrees
        self.update_position_trans = 1  # inches

    def move_to_start(self):
        print(' go to start')
        above = True
        while above:
            self.translate_down()
            above = self.check_for_bottom()

    def rotate_left(self):
        print('lefting')
        # step motor left
        self.position[0] -= self.update_position_rot

    def rotate_right(self):
        print('righting')
        # step motor right
        # wait update position
        self.position[0] += self.update_position_rot

    def translate_up(self):
        print('upping')
        # step up one ??
        self.position[1] -= self.update_position_trans

    def translate_down(self):
        print('downing')
        # step down one ??
        self.position[1] += self.update_position_trans

    def reset(self):
        print('reset')
        # step until back to center
        # step until at top
        self.position = [0, 0]
        return True

    def check_for_bottom(self):
        print('hit it!')
        return False

    def check_full_circle(self):
        print('went around')
        return False

    def check_scan_complete(self):
        print('idk how we do this')
        return False
