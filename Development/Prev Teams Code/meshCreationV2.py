import numpy as np
import open3d as o3d
import open3d.cpu.pybind.geometry as cpu_geom

class MeshGenerator:
    def __init__(self, dataname):
        self.dataname = dataname
        self.point_cloud = None
        self.pcd = None
        self.poisson_mesh = None
        self.bbox = None
        self.p_mesh_crop = None
        
    def load_point_cloud(self):
       try:
            self.point_cloud = np.loadtxt(self.dataname, skiprows=1)
       except Exception as e:
            print("Loading Error: "+ e.args)
        
    # sets normals and loads in the points from the point cloud    
    def create_point_cloud(self):
        try:
            if self.point_cloud is None:
                self.load_point_cloud()
            self.pcd = o3d.geometry.PointCloud()
            self.pcd.points = o3d.utility.Vector3dVector(self.point_cloud)
            # self.pcd.normals = o3d.utility.Vector3dVector(self.point_cloud[:,:3])
            self.pcd.estimate_normals()
            self.pcd.orient_normals_consistent_tangent_plane(20)
        except Exception as e:
            print("Point Cloud Error: "+ e.args)
        
    def view_point_cloud(self):
        try:
            o3d.visualization.draw_geometries([self.pcd])
        except Exception as e:
            print("Visulatization Error: "+ e.args)
        
    def create_mesh(self):
        try:
            if self.pcd is None:
                self.create_point_cloud()
            self.poisson_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(self.pcd, depth=9, width=0, scale=1, linear_fit=True)[0]
            self.poisson_mesh = o3d.geometry.TriangleMesh.compute_triangle_normals(self.poisson_mesh)
        except Exception as e:
            print("Problem Creating Mesh: "+ e.args)
        
    #does bad currently
    def crop_mesh_to_point_cloud_bounding_box(self):
        try:
            if self.poisson_mesh is None:
                self.create_mesh()
            self.bbox = self.pcd.get_axis_aligned_bounding_box()
            self.p_mesh_crop = self.poisson_mesh.crop(self.bbox)
        except Exception as e:
            print("Croping Mesh Error: "+ e.args)
            
    def save_mesh_to_file(self, filename):
        try:
            if self.p_mesh_crop is None:
                self.crop_mesh_to_point_cloud_bounding_box()
            o3d.io.write_triangle_mesh(filename, self.poisson_mesh) #supposed to be self.p_mesh_crop instead of poisson mesh but that caused holes in the 3d model
        except Exception as e:
            print("Saving Error: "+ e.args)     
            
    def save_cropped_mesh_to_file(self, filename):
        try:
            if self.p_mesh_crop is None:
                self.crop_mesh_to_point_cloud_bounding_box()
            o3d.io.write_triangle_mesh(filename, self.p_mesh_crop) #supposed to be self.p_mesh_crop instead of poisson mesh but that caused holes in the 3d model
        except Exception as e:
            print("Saving Cropped Mesh Error: "+ e.args)
            
    def check_open3d_version(self):
        print(o3d.__version__)
        
    def display_mesh(self):
        o3d.visualization.draw_geometries([self.poisson_mesh])
        
        
if __name__ == '__main__':
    
    dataname = "Prev Teams Code\\pointCloud3.xyz"
    mesh = MeshGenerator(dataname)
    mesh.load_point_cloud()
    mesh.create_point_cloud()
    mesh.view_point_cloud()
    mesh.create_mesh()
    #mesh.crop_mesh_to_point_cloud_bounding_box()
    mesh.display_mesh()
    mesh.save_mesh_to_file("pC_mesh_c.stl")
    mesh.save_cropped_mesh_to_file("pC_cropped_mesh_c.stl")
