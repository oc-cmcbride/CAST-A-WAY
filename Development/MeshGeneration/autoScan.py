"""
manualScan.py
"""
import open3d as o3d
from imageTools import *


class MeshCreate:
    def __init__(self):
        self.badMesh = False
        self.points3d = []
        self.pointCloud = o3d.geometry.PointCloud()

    def create_point_cloud(self):
        try:
            self.pointCloud.points = o3d.utility.Vector3dVector(self.points3d)
        except Exception as e:
            print(f"Error making point cloud: {e}")
            self.badMesh = True

        # Estimate normals
        try:
            self.pointCloud.estimate_normals()
            self.pointCloud.orient_normals_consistent_tangent_plane(20)
        except Exception as e:
            print(f"Error estimating normals: {e}")
            self.badMesh = True

    def create_mesh(self):
        try:
            self.mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
                self.pointCloud,
                depth=9,
                width=0,
                scale=1,
                linear_fit=True
            )[0]
            self.mesh = o3d.geometry.TriangleMesh.compute_triangle_normals(self.mesh)
        except Exception as e:
            print(f"Error creating mesh: {e}")
            self.badMesh = True

        # Display mesh
        if not self.badMesh:
            # Show point cloud
            # o3d.visualization.draw_geometries([pointCloud])

            # Paint mesh (to make it easier to see) and draw
            self.mesh.paint_uniform_color([0.5, 0.5, 0.5])
            o3d.visualization.draw_geometries(
                geometry_list=[self.pointCloud, self.mesh],
                mesh_show_wireframe=True,
                mesh_show_back_face=True
            )

    def write_file(self):
        o3d.io.write_triangle_mesh(MESH_FILE_NAME, self.mesh)
