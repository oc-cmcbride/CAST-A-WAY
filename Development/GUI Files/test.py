import sys
import numpy as np
from PyQt5.QtWidgets import QApplication
from pyqtgraph.opengl import GLViewWidget, MeshData, GLMeshItem, GLScatterPlotItem
from stl import mesh

def center_mesh(vertices):
    centroid = np.mean(vertices, axis=0)
    return vertices - centroid

def get_bottom_center(mesh_data):
    min_y = np.min(mesh_data.vertexes()[:, 1])
    bottom_vertices = mesh_data.vertexes()[np.isclose(mesh_data.vertexes()[:, 1], min_y)]
    return np.mean(bottom_vertices, axis=0)

class CustomGLViewWidget(GLViewWidget):
    def __init__(self, stl_file):
        super().__init__()

        stl_mesh = mesh.Mesh.from_file(stl_file)

        points = stl_mesh.points.reshape(-1, 3)
        centered_points = center_mesh(points)
        faces = np.arange(centered_points.shape[0]).reshape(-1, 3)

        mesh_data = MeshData(vertexes=centered_points, faces=faces)

        # Set color of the mesh to black and enable drawing faces
        self.mesh = GLMeshItem(meshdata=mesh_data, color=(0, 0, 0, 1), smooth=True, drawFaces=True, drawEdges=True)
        self.addItem(self.mesh)

        # Find center of the bottom face
        bottom_center = get_bottom_center(mesh_data)

        # Create a dot at the center of the bottom face
        self.dot = GLScatterPlotItem(pos=np.array([bottom_center]), size=10, color=(0, 255, 0, 255))  # RGBA: green
        self.addItem(self.dot)

        self.opts['distance'] = 50
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = CustomGLViewWidget('cube.stl')
    sys.exit(app.exec_())
