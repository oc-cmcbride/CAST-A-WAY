from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialog


class loadPopUpScreen(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(100, 100, 1600, 1200)
        self.loading_label = QLabel(self)
        self.movie = QMovie("200w.gif")  # Replace "spinner.gif" with the path to your animated GIF

        layout = QVBoxLayout(self)
        layout.addWidget(self.loading_label)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setMovie(self.movie)
        self.setLayout(layout)

    def showPopup(self):
        self.show()
        self.movie.start()

    def close(self):
        self.reject()


class errorPopUpScreen(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(100, 100, 1600, 1200)

    def close(self):
        self.reject()
