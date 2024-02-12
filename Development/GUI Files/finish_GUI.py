import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, \
    QLabel, QLineEdit, QFormLayout, QPushButton


class finishedScreen(QFrame):

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.setGeometry(100, 100, 1600, 1200)

        self.save_button = QPushButton('Save File')
        self.save_button.setMaximumWidth(300)
        self.save_button.clicked.connect(self.save_file)
        button_menu = QHBoxLayout()
        button_menu.addWidget(self.save_button)

        self.another_scan_button = QPushButton('Another Scan')
        self.another_scan_button.setMaximumWidth(300)
        self.another_scan_button.clicked.connect(self.window.home_click)
        button_menu.addWidget(self.another_scan_button)

        self.finish_session_button = QPushButton('Finish Session')
        self.finish_session_button.setMaximumWidth(300)
        self.finish_session_button.clicked.connect(self.window.login_click)
        button_menu.addWidget(self.finish_session_button)
        button_menu.setAlignment(Qt.AlignCenter)

        self.setLayout(button_menu)

    def save_file(self):
        self.save_button.setText("file saved")
