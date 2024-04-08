"""
Morgan Demuth
March 25, 2024
Systems Engineering Design
Team CAST-A-WAY

This program is the main program GUI that runs a Qwindow that switches between widgets
"""
from PyQt5.QtWidgets import QWidget, QMainWindow, QStackedWidget, QVBoxLayout
from GUIFiles.loginGUI import loginScreen
from GUIFiles.homeGUI import homeScreen
from GUIFiles.finishGUI import finishedScreen


class MainWindow(QMainWindow):

    def __init__(self, main_program):
        super().__init__()
        self.setGeometry(100, 100, 1600, 1200)
        self.setWindowTitle("CAST-A-WAY")
        self.main_program = main_program

        # Create the central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create the stacked widget
        self.stacked_widget = QStackedWidget(self.central_widget)
        self.stacked_widget.resize(900, 900)
        self.login = loginScreen(self)
        self.home = homeScreen(self)
        self.finished = finishedScreen(self)
        self.add_login_frame()
        self.add_home_frame()
        self.add_finished_frame()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.central_widget.setLayout(main_layout)
        self.home_click()

    def add_login_frame(self):
        self.stacked_widget.addWidget(self.login)

    def add_home_frame(self):
        self.stacked_widget.addWidget(self.home)

    def add_finished_frame(self):
        self.stacked_widget.addWidget(self.finished)

    def login_click(self):
        self.stacked_widget.setCurrentIndex(0)
        self.login.reset()

    def home_click(self):
        self.stacked_widget.setCurrentIndex(1)
        self.home.reset()
        self.home.calibrate()

    def finish_click(self):
        self.stacked_widget.setCurrentIndex(2)
        self.finished.reset()

    def start_clicked(self):
        self.main_program.start()

    def get_file_name(self):
        file_name = self.main_program.get_file()
        return file_name
