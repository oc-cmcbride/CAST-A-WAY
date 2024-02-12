import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAction, QMenu, QFrame, QApplication, QWidget, QMainWindow, QStackedWidget, QVBoxLayout
from login_GUI import loginScreen
from home_GUI import homeScreen
from popup_GUI import loadPopUpScreen
from finish_GUI import finishedScreen


class MainWindow(QMainWindow):

    def __init__(self, main_prog):
        super().__init__()
        self.setGeometry(100, 100, 1600, 1200)
        self.setWindowTitle("CAST-A-WAY")
        self.main_prog = main_prog

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
        self.finish_click()

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

    def finish_click(self):
        self.stacked_widget.setCurrentIndex(2)

    def start_clicked(self):
        self.main_prog.start()
