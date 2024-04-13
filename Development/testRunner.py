import open3d as o3d
from MeshGeneration.autoScan import MeshCreate
from MeshGeneration.dataCollection import DataCollection

def GetImages(dc: DataCollection):
    dc.get_images()
    print("done'd")

def GetPoints(dc: DataCollection):
    dc.index_picture = 55
    dc.get_image_points()
    print("done'd again")

def GenerateMesh(mc: MeshCreate, points3d):
    mc.points3d = points3d
    mc.create_point_cloud()
    mc.create_mesh()

def main():
    dc = DataCollection()
    mc = MeshCreate()
    # GetImages(dc)
    GetPoints(dc)
    GenerateMesh(mc, dc.points3d)

if __name__ == "__main__":
    main()
