import os
print(os.getcwd())

import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from GUIFiles.mainGUI import MainWindow
from MeshGeneration.autoScan import MeshCreate


class FinalProgram:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow(self)
        self.mesh = MeshCreate()

    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())

    def start(self):
        self.mesh.start()
        print('Started')

    def get_file(self):
        return 'mesh'


# call reset

# call scan

# call mesh creation

# error requests?


if __name__ == '__main__':
    final_code = FinalProgram()
    final_code.run()
