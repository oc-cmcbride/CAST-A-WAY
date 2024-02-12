'''
imageTools.py

Colin McBride, adapted from code by Morgan Demuth and Noah Doner
Jan 24, 2024
Systems Engineering Design
Team CAST-A-WAY

This program provides various functions and tools used to aid in 
image capturing and processing. A summary of each tool can be 
found above its definition. 

The tools available in this file are: 
- 
'''
from dataclasses import dataclass
import cv2
import numpy as np
import matplotlib.pyplot as plt


'''
CameraLaserConfig
Structure that contains all important configuration data about the camera/laser 
setup. 
'''
@dataclass
class CameraLaserConfig:
    xmax: float         # Image width in pixels 
    ymax: float         # Image height in pixels 
    thetaFov: float     # Horizontal camera field of view in radians 
    dLaser: float       # Distance between the laser and camera lens
    thetaLaser: float   # Angle of the laser around the 3D Z axis
    phiLaser: float     # Angle of the laser around the 3D Y axis
# end class CameraLaserConfig

'''
setupVideoCapture()
Sets up a video capture object using the specified video device and 
returns the capture object. 
'''
def setupVideoCapture(devIndex:int=1, width:int=1280, height:int=720, verbose=False):
    # Get video capture object
    if verbose:
        print("Acquiring camera resource...")
    cap = cv2.VideoCapture(devIndex)

    # Set aspect ratio
    if verbose:
        print("Setting camera width...")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    if  verbose:
        print("Setting camera height...")
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    if verbose:
        print("Video capture object set up!")

    # Return object
    return cap
# end setupVideoCapture()

'''
detectLine()
Detects a single red laser line in the given image frame. 
'''
def detectLine(image:np.ndarray, threshold_value:int=200):
    # Extract the red channel
    red_channel = image[:, :, 2]

    # Apply a threshold to detect the laser line 
    _, binary = cv2.threshold(red_channel, threshold_value, 255, cv2.THRESH_BINARY)

    # Find the position with the most white pixels (highest brightness) in each row
    center_points = []

    # Loop through all rows of pixels
    for y in range(binary.shape[0]):
        # Find all white x values in the current row
        row = binary[y, :]
        white_x = np.where(row > 0)[0]

        # Find the average x-coordinate of the white points
        if len(white_x) > 0:
            # At least one white point exists 
            # Find average x-coordinate
            x = int(np.mean(white_x))
            center_points.append((x, y))
        # end if len
    # end for y in range

    # Return points along the laser line 
    return center_points
# end detectLine()

'''
calculateImagePointDepth()
Takes in an image point and camera configuration data and outputs the 
estimated depth value. 
'''
def calculateImagePointDepth(x:float, y:float, clc:CameraLaserConfig) -> float:
    return (clc.dLaser) / (np.tan(clc.thetaLaser) + np.tan(clc.thetaFov * ((x - (y - 0.5*clc.ymax)*np.tan(clc.phiLaser)) / (clc.xmax) - 0.5)))
# end calculateImagePointDepth()

'''
imageToCameraCoords()
Takes a set of image coordinate parameters (x, y, width, height, hfov) and 
depth and converts them to a 3D coordinate (x, y, z) relative to the camera. 
'''
def imageToCameraCoords(x:float, y:float, depth:float, clc:CameraLaserConfig):
    # Calculate vertical FOV
    hfov = clc.thetaFov
    vfov = hfov * clc.ymax / clc.xmax

    # Calculate 3D coordinates
    x3d = (x / clc.xmax - 0.5) * (2 * depth * np.tan(0.5*hfov))
    y3d = depth
    z3d = (0.5 - y / clc.ymax) * (2 * depth * np.tan(0.5*vfov))

    # Return results 
    return [x3d, y3d, z3d]
# end imageToCameraCoords

'''
plotPointCloud()
Takes a list of 3D points and displays a 3D plot. 

points: A list of 3D points, either in list or tuple format 
blocking: Whether or not the function will block when displaying the plot 
'''
def plotPointCloud(points, blocking=True):
    # Create figure and axes
    fig = plt.figure()
    ax = plt.axes(projection="3d")

    # Format axes
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # Transpose data
    [x, y, z] = list(zip(*points))

    # Add data to plot 
    ax.scatter(x, y, z)

    # Show final plot
    plt.show(block=blocking)
# end plotPointCloud

'''
writePointsToFile()
Takes a list of 3D coordinates (3-element float tuples) and outputs them to 
a specified destination file. The contents are output in the format below, 
with spaces as delimiters: 
{x1} {y1} {z1}
{x2} {y2} {z2}
...

If a file with the given name already exists, the contents will be overwritten. 

points: List of 3D points
dest: Destination file name. Should include the ".xyz" extension. 
'''
def writePointsToFile(points, dest:str):
    with open(dest, "w") as file:
        for point in points:
            file.write(f"{point[0]} {point[1]} {point[2]}")
# end writePointsToFile
