# imports
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from main_GUI import MainWindow
#from mesh import MeshCreate


class FinalProgram:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow(self)
        #self.mesh_create = MeshCreate()

    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())

    def start(self):
        self.calibrate()
        #self.mesh_create.run()
        print('Started')

    def calibrate(self):
        timer = QTimer(self.window)
        timer.timeout.connect()
        timer.start(10000)

# call reset

# call scan

# call mesh creation

# get stl file

# error requests?


if __name__ == '__main__':
    final_code = FinalProgram()
    final_code.run()
