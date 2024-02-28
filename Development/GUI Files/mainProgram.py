import sys
import os
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from mainGUI import MainWindow


class FinalProgram:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow(self)

    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())

    def start(self):
        self.calibrate()
        print('Started')

    def calibrate(self):
        timer = QTimer(self.window)
        timer.timeout.connect()
        timer.start(10000)

    def get_file(self):
        return 'mesh'


# call reset

# call scan

# call mesh creation

# error requests?


if __name__ == '__main__':
    final_code = FinalProgram()
    final_code.run()
