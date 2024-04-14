"""
Morgan Demuth
March 25, 2024
Systems Engineering Design
Team CAST-A-WAY

This program is the GUI file that opperates the finish screen as well as the display for the mesh
"""
import shutil
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QPushButton
import numpy as np
from pyqtgraph.opengl import GLViewWidget, MeshData, GLMeshItem
from stl import mesh
import os


class finishedScreen(QFrame):

    def __init__(self, window):
        super().__init__()
        self.file_name = None
        self.file_path = None
        self.mesh = None
        # self.directory_path = r'C:\Users\medem\OneDrive\Documents\GitHub\CAST-A-WAY\Development\MeshGeneration'
        self.directory_path = os.getcwd() + r'\Development\MeshGeneration'
        self.window = window
        self.setGeometry(100, 100, 1600, 1200)

        self.get_mesh()
        self.mesh.setFixedSize(1600, 1000)
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

        layout = QVBoxLayout()
        layout.addWidget(self.mesh)
        layout.addLayout(button_menu)
        self.setLayout(layout)

    def save_file(self):
        folder_path = r"C:\Users\medem\OneDrive\Documents\GitHub\CAST-A-WAY\Development\GUI Files\finalSTL"

        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # List files in the folder
        files = os.listdir(folder_path)
        num_files = len(files)

        # Generate the new file name based on the number of existing files
        index = num_files + 1
        file_name_path = f'{self.file_name}{index}.stl'

        # Create the full file path for the new file
        new_file_path = os.path.join(folder_path, file_name_path)

        # Copy the file to the new location
        shutil.copy(self.file_path, new_file_path)

        # Update the button text
        self.save_button.setText("File saved")

    def get_mesh(self):
        # Create the full file path
        self.file_name = self.window.get_file_name()
        file_name_with_extension = f'{self.file_name}.stl'
        self.file_path = os.path.join(self.directory_path, file_name_with_extension)
        self.mesh = CustomGLViewWidget(self.file_path)

    def reset(self):
        self.save_button.setText('Save File')


class CustomGLViewWidget(GLViewWidget):
    def __init__(self, stl_file):
        super().__init__()
        self.setBackgroundColor('w')
        # Set background color to white
        stl_mesh = mesh.Mesh.from_file(stl_file)
        self.points = stl_mesh.points.reshape(-1, 3)
        centered_points = self.center_mesh()
        faces = np.arange(centered_points.shape[0]).reshape(-1, 3)

        self.mesh_data = MeshData(vertexes=centered_points, faces=faces)

        # Create mesh item with black edges
        self.mesh = GLMeshItem(meshdata=self.mesh_data, color=(0, 0, 0, 1), drawFaces=False, drawEdges=True)
        self.addItem(self.mesh)

        # front_center = self.get_front_center()

        # Create a dot at the center of the front face
        """dot_mesh_data = MeshData.sphere(rows=10, cols=10, radius=0.1)
        self.dot = GLMeshItem(meshdata=dot_mesh_data, color=(0, 255, 0, 255))  # RGBA: green
        self.dot.translate(front_center[0], front_center[1], front_center[2])  # Translate to front center
        self.addItem(self.dot)"""

        self.opts['distance'] = 50
        self.show()

    def center_mesh(self):
        centroid = np.mean(self.points, axis=0)
        return self.points - centroid

    """def get_front_center(self):
        front_face_index = np.argmin(self.mesh_data.vertexes()[:, 2])
        front_face_vertices = self.mesh_data.faces()[front_face_index]

        # Calculate the center of the bounding box of the front face
        front_face_points = self.mesh_data.vertexes()[front_face_vertices]
        min_point = np.min(front_face_points, axis=0)
        max_point = np.max(front_face_points, axis=0)
        front_center = (min_point + max_point) / 2

        return front_center"""
