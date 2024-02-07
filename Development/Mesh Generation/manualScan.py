'''
manualScan.py

Colin McBride
Jan 31, 2024
Systems Engineering Design
Team CAST-A-WAY

This program takes in a set of images taken with a certain 
offset and then generates a mesh from the points detected in 
the images. 

When generating the mesh, the samples are assumed to be 
taken from equidistant intervals. There are variables that 
change the direction the points are stacked: 
  X: Right(+)/Left(-) from the camera's perspective 
  Y: Forward(+)/Backward(-) from the camera's perspective
  Z: Up(+)/Down(-) from the camera's perspective 
'''
import numpy as np
import open3d as o3d
from imageTools import *

'''
CONSTANTS
'''
# Image folder properties
IMG_FOLDER = "test2photos\\"
NUM_IMAGES = 12

# Camera parameters
WIDTH = 1280
HEIGHT = 720
H_FOV = 55
D_LASER = 3.125
THETA_LASER = 55
PHI_LASER = 90-66.5
BRIGHT_THRESH = 200

# Model generation parameters
#               X, Y, Z
POINT_OFFSET = [0.1, 0.1, 0]
WRITE_MESH_TO_FILE = True
MESH_FILE_NAME = "mesh.stl"

'''
MAIN
'''
def main():
    # Set up camera/laser config data
    clConfig = CameraLaserConfig(
        WIDTH, 
        HEIGHT, 
        np.deg2rad(H_FOV),
        D_LASER,
        np.deg2rad(THETA_LASER),
        np.deg2rad(PHI_LASER)
    )

    # Initialize 3D points list
    # This list contains 3-element tuples
    points3d = []

    # Read in frames from image files
    frames = []
    for i in range(NUM_IMAGES):
        frames.append(cv2.imread(f"{IMG_FOLDER}capture{i:03d}.png"))

    # Keep track of which frame is being scanned
    frameCount = 0

    # Read in points from frames
    print("Processing with the following parameters:")
    print(f"Resolution: {clConfig.xmax} x {clConfig.ymax}")
    print(f"Camera horizontal FOV: {clConfig.thetaFov:.4f} rad")
    print(f"Laser distance: {clConfig.dlaser}")
    print(f"Laser rotation: Z-axis: {clConfig.thetaLaser:.4f} rad, Y-axis: {clConfig.phiLaser:.4f} rad")
    for frame in frames:
        # Calculate new points
        points2d = detectLine(frame, BRIGHT_THRESH)

        # Downsample the detected points to improve mesh generation
        points2d = points2d[::10]

        # Convert 2d image points to 3d points
        for [x, y] in points2d:
            depth = calculateImagePointDepth(x, y, clConfig)
            newPoint = imageToCameraCoords(x, y, depth, clConfig)

            # Apply offset
            newPoint[0] += POINT_OFFSET[0] * frameCount
            newPoint[1] += POINT_OFFSET[1] * frameCount
            newPoint[2] += POINT_OFFSET[2] * frameCount

            # Add to point list
            points3d.append(newPoint)
        # end for [x,y] in points2d
        
        # Increment frame count
        frameCount += 1
    # end for frame in frames


    # Generate 3D model from the saved points
    # Control variable for successful mesh creation
    badMesh = False

    # Create point cloud object
    try:
        pointCloud = o3d.geometry.PointCloud()
        pointCloud.points = o3d.utility.Vector3dVector(points3d)
    except Exception as e:
        print(f"Error making point cloud: {e}")
        badMesh = True

    # Estimate normals
    try:
        pointCloud.estimate_normals()
        pointCloud.orient_normals_consistent_tangent_plane(20)
    except Exception as e:
        print(f"Error estimating normals: {e}")
        badMesh = True

    # Create mesh
    try:
        mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
            pointCloud,
            depth=9,
            width=0,
            scale=1,
            linear_fit=True
        )[0]
        mesh = o3d.geometry.TriangleMesh.compute_triangle_normals(mesh)
    except Exception as e:
        print(f"Error creating mesh: {e}")
        badMesh = True
    
    # Display mesh
    if not badMesh:
        # Show point cloud
        #o3d.visualization.draw_geometries([pointCloud])

        # Paint mesh (to make it easier to see) and draw
        mesh.paint_uniform_color([0.5, 0.5, 0.5])
        o3d.visualization.draw_geometries(
            geometry_list = [pointCloud, mesh],
            mesh_show_wireframe = True,
            mesh_show_back_face = True
        )

        # Write mesh to file if desired
        if WRITE_MESH_TO_FILE:
            o3d.io.write_triangle_mesh(MESH_FILE_NAME, mesh)
# end main


if __name__ == "__main__":
    main()
