import sys

from PyQt5.QtGui import QVector3D
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.Qt3DExtras import Qt3DWindow
from PyQt5.Qt3DCore import QEntity
from PyQt5.Qt3DRender import QMesh
from PyQt5.QtCore import QUrl

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("STL Viewer")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create the Qt3D window
        self.view = Qt3DWindow()
        self.container = QWidget.createWindowContainer(self.view)
        layout.addWidget(self.container)

        # Root entity
        self.rootEntity = QEntity()
        self.view.setRootEntity(self.rootEntity)

        # Camera
        self.camera = self.view.camera()
        self.camera.lens().setPerspectiveProjection(45.0, 16.0/9.0, 0.1, 1000.0)
        self.camera.setPosition(QVector3D(0, 0, 40))
        self.camera.setViewCenter(QVector3D(0, 0, 0))

        # Load and display the STL file
        self.loadSTLFile("cube.stl")

    def loadSTLFile(self, filename):
        meshEntity = QEntity(self.rootEntity)
        mesh = QMesh()
        mesh.setSource(QUrl.fromLocalFile(filename))
        meshEntity.addComponent(mesh)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
