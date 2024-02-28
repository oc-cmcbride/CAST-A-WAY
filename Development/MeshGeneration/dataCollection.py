"""
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
"""
from imageTools import *

"""
CONSTANTS
"""

# Image folder properties
IMG_FOLDER = "test2photos\\"
NUM_IMAGES = 12

# Camera parameters
WIDTH = 1280
HEIGHT = 720
H_FOV = 55
D_LASER = 3.125
THETA_LASER = 12.5
PHI_LASER = 90 - 66.5
BRIGHT_THRESH = 200

# Model generation parameters
#               X, Y, Z
POINT_OFFSET = [1, 0, 0]
WRITE_MESH_TO_FILE = True
MESH_FILE_NAME = "mesh.stl"

class DataCollection:
    def __init__(self):
        # Set up camera/laser config data
        self.clConfig = CameraLaserConfig(
            WIDTH,
            HEIGHT,
            np.deg2rad(H_FOV),
            D_LASER,
            np.deg2rad(THETA_LASER),
            np.deg2rad(PHI_LASER)
        )
        self.points3d = []
        # Initialize 3D points list
        # This list contains 3-element tuples
    def get_images(self):

    def get_image_points(self):
        # Read in frames from image files
        frames = []
        for i in range(NUM_IMAGES):
            frames.append(cv2.imread(f"{IMG_FOLDER}capture{i:03d}.png"))

        # Keep track of which frame is being scanned
        frameCount = 0

        # Read in points from frames
        print("Processing with the following parameters:")
        print(f"Resolution: {self.clConfig.xmax} x {self.clConfig.ymax}")
        print(f"Camera horizontal FOV: {self.clConfig.thetaFov:.4f} rad")
        print(f"Laser distance: {self.clConfig.dlaser}")
        print(f"Laser rotation: Z-axis: {self.clConfig.thetaLaser:.4f} rad, Y-axis: {self.clConfig.phiLaser:.4f} rad")
        for frame in frames:
            # Calculate new points
            points2d = detectLine(frame, BRIGHT_THRESH)

            # Downsample the detected points to improve mesh generation
            points2d = points2d[::10]

            # Convert 2d image points to 3d points
            for [x, y] in points2d:
                depth = calculateImagePointDepth(x, y, self.clConfig)
                newPoint = imageToCameraCoords(x, y, depth, self.clConfig)

                # Apply offset
                newPoint[0] += POINT_OFFSET[0] * frameCount
                newPoint[1] += POINT_OFFSET[1] * frameCount
                newPoint[2] += POINT_OFFSET[2] * frameCount

                # Add to point list
                self.points3d.append(newPoint)
            # end for [x,y] in points2d

            # Increment frame count
            frameCount += 1
        # end for frame in frames


