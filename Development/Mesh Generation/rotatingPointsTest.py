'''
rotatingPointsTest.py

Colin McBride
Feb 28, 2024
Systems Engineering Design
Team CAST-A-WAY

This program tests rotating a matrix of points to make a cylindrical point 
cloud. 
'''
import numpy as np
import open3d as o3d
from imageTools import *

'''
CONSTANTS
'''
# Image file path
IMAGE_FILE = "Development\\Mesh Generation\\test2photos\\capture003.png"

# Camera parameters
WIDTH = 1280
HEIGHT = 720
H_FOV = 55
D_LASER = 3.28
THETA_LASER = 13.22
PHI_LASER = 22.71
BRIGHT_THRESH = 200

# Model generation parameters
NUM_STEPS = 10
ROT_INIT = [0, 0, 0]
ROT_STEP = [0, 0, 10]

'''
MAIN
'''
def main():
    # Initialize camera/laser config
    config = CameraLaserConfig(
        WIDTH, 
        HEIGHT, 
        np.deg2rad(H_FOV),
        D_LASER,
        np.deg2rad(THETA_LASER),
        np.deg2rad(PHI_LASER)
    )

    # Initialize 3D points list
    points3d = []

    # Read in frame from image file
    frame = cv2.imread(IMAGE_FILE)

    # Calculate 2D points and camera coords
    points2d = detectLine(frame, BRIGHT_THRESH)
    points2d = points2d[::10]
    cameraCoords = [imageToCameraCoords(x, y, calculateImagePointDepth(x, y, config), config) for (x, y) in points2d]

    # Apply offsets
    for (x, y, z) in cameraCoords:
        # Duplicate the point for the number of specified steps 
        for i in range(NUM_STEPS):
            # Calculate angles
            alpha = np.deg2rad(i * ROT_STEP[0] + ROT_INIT[0])
            gamma = np.deg2rad(i * ROT_STEP[2] + ROT_INIT[2])

            # Generate arrays for multiplication
            Pcc = [ # Point Camera Coordinate
                [x],
                [y],
                [z]
            ]
            Rx = [ # Rotation x matrix
                [1, 0, 0],
                [0, np.cos(alpha), -np.sin(alpha)],
                [0, np.sin(alpha), np.cos(alpha)]
            ]
            Rz = [ # Rotation z matrix
                [np.cos(gamma), -np.sin(gamma), 0],
                [np.sin(gamma), np.cos(gamma), 0],
                [0, 0, 1]
            ]

            # Perform multiplications to get world coordinates (z rotation, then x rotation)
            Pwc = np.matmul(Rx, Pcc)
            Pwc = np.matmul(Rz, Pwc)

            # Unpack and add point to 3D points
            newPoint = [p[0] for p in Pwc]
            points3d.append(newPoint)
        # end for i
    # end for (x, y, z)
    
    # Generate 3D model from the saved points
    # Control variable for successful mesh creation
    badMesh = False

    # Create point cloud object
    try:
        pointCloud = o3d.geometry.PointCloud()
        pointCloud.points = o3d.utility.Vector3dVector(points3d)
        # Remove outliers
        # pointCloud, _ = pointCloud.remove_statistical_outlier(nb_neighbors=20, std_ratio=3.0)
        # pointCloud, _ = pointCloud.remove_radius_outlier(nb_points=10, radius=2)
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
        '''
        mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
            pcd=pointCloud,
            depth=9,
            width=0,
            scale=1,
            linear_fit=True
        )[0]
        
        '''
        mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
            pcd=pointCloud,
            radii=o3d.utility.DoubleVector([1, 1.25, 1.5, 2])
        )
        
        '''
        mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(
            pcd=pointCloud,
            alpha=1.1
        )
        '''

        # Required for rendered shading
        mesh = o3d.geometry.TriangleMesh.compute_triangle_normals(mesh)
    except Exception as e:
        print(f"Error creating mesh: {e}")
        badMesh = True
    # end try
    
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
    # end if not badMesh
    
# end main
    
'''
Call main
'''
if __name__ == "__main__":
    main()
