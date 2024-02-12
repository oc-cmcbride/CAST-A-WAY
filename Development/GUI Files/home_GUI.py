import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, \
    QLabel, QLineEdit, QFormLayout, QPushButton
from qtpy import QtCore
from popup_GUI import loadPopUpScreen


class homeScreen(QFrame):

    def __init__(self, window):
        super().__init__()
        self.setGeometry(100, 100, 1600, 1200)
        self.window = window
        self.popup = loadPopUpScreen()
        heading_font = QFont('Times New Roman', 35)
        subheading_font = QFont('Times New Roman', 20)

        angle_label = QLabel('Laser Angle')
        self.angle_entry = QLineEdit()
        degree_label = QLabel('degrees')
        angle = QHBoxLayout()
        angle.addWidget(angle_label)
        angle.addWidget(self.angle_entry)
        angle.addWidget(degree_label)

        self.start_button = QPushButton('Start')
        self.start_button.setMaximumWidth(200)
        self.start_button.clicked.connect(self.start)

        self.quit_button = QPushButton('Quit')
        self.quit_button.setMaximumWidth(200)
        self.quit_button.clicked.connect(self.quit)
        button_menu = QHBoxLayout()
        button_menu.addWidget(self.quit_button)
        self.quit_button.setVisible(False)

        self.restart_button = QPushButton('Restart')
        self.restart_button.setMaximumWidth(200)
        self.restart_button.clicked.connect(self.restart)
        button_menu.addWidget(self.restart_button)
        self.restart_button.setVisible(False)

        self.finish_button = QPushButton('Finish')
        self.finish_button.setMaximumWidth(200)
        self.finish_button.clicked.connect(self.window.finish_click)
        button_menu.addWidget(self.finish_button)
        button_menu.setAlignment(Qt.AlignLeft)
        self.finish_button.setVisible(False)

        self.logout_button = QPushButton('Logout')
        self.logout_button.setMaximumWidth(200)
        self.logout_button.clicked.connect(self.window.login_click)
        self.display = QLabel('Display')
        self.display.setFont(heading_font)

        left = QVBoxLayout()
        left.addLayout(angle)
        left.addWidget(self.start_button)
        left.addLayout(button_menu)
        left.setAlignment(Qt.AlignLeft)
        right = QVBoxLayout()
        right.addWidget(self.logout_button)
        right.addWidget(self.display)
        right.setAlignment(Qt.AlignRight)
        layout = QHBoxLayout()
        layout.addLayout(left)
        layout.addLayout(right)
        self.setLayout(layout)

    def start(self):
        self.popup.showPopup()
        self.window.start_clicked()
        self.start_button.setVisible(False)
        self.quit_button.setVisible(True)
        self.restart_button.setVisible(True)
        self.finish_button.setVisible(True)

    def quit(self):
        self.start_button.setVisible(True)
        self.quit_button.setVisible(False)
        self.restart_button.setVisible(False)
        self.finish_button.setVisible(False)

    def restart(self):
        self.window.start_clicked()
        self.popup.exec_()
        self.start_button.setVisible(False)
        self.quit_button.setVisible(True)
        self.restart_button.setVisible(True)
