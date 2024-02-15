'''
imageToolsTest.py
Colin McBride
Jan 24, 2024
Systems Engineering Design
Team CAST-A-WAY

This program is intended to test the various functions in imageTools.py. 
'''
# Imports
from imageTools import *
import cv2
import numpy as np

'''
test1()

This tests the detectLine function. 
This also calculates a line of best fit on the line in the image and 
outputs the line slope (m), offset(b), and angle in degrees. 
'''
def test1(fileName:str, threshold:int = 200):
    # Read in image
    frame = cv2.imread(fileName)

    # Detect points along the line 
    points = detectLine(frame, threshold)

    # Extract x and y points
    transposedPoints = list(zip(*points))

    # Calculate best fit line
    m, b = np.polyfit(transposedPoints[0], transposedPoints[1], 1)

    # Plot points on image
    for point in points:
        cv2.circle(frame, point, 2, (255, 0, 0), -1)

    # Plot best fit line on image
    # (We iterate over the y coordinates because the detectLine function
    # scans each row of pixels, ensuring there will always be at least 1 
    # point for every y coordinate)
    for y in transposedPoints[1]:
        cv2.circle(frame, (int((y - b) / m), y), 1, (0, 255, 0), -1)
    
    # Calculate angle of laser from best fit line
    angle = np.arctan(-m) * (180 / np.pi)

    # Print results
    print(f"Best fit line (y = m*x + b): m = {m}, b = {b}")
    print("(m and b are relative to image coordinates, where (0,0) is in the top left")
    print("and the y coordinate increases going down instead of up.)")
    print(f"Angle: {angle} deg")

    # Display image
    cv2.imshow("Frame", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
# end test1()


'''
test2()

This test takes in an image and parameters for the depth equation and 
prints the calculated depth at each point. 
'''
def test2(dlaser:float, thetaLaser:float, thetaFov:float, phiLaser:float, fileName:str, brightnessThreshold:int = 200):
    # Read in image
    frame = cv2.imread(fileName)

    # Find image dimensions
    xmax = frame.shape[1]
    ymax = frame.shape[0]

    # Detect points along the line
    points = detectLine(frame, brightnessThreshold)

    # Calculate depth values
    depths = []
    for [x, y] in points:
        depths.append((dlaser) / (np.tan(thetaLaser) + np.tan(thetaFov * ((x - (y - 0.5*ymax)*np.tan(phiLaser)) / (xmax) - 0.5))))
    
    # Print depth values
    
    for d in depths:
        print(f"{d:03f}\t", end="")
    print()
    
    
    # Print midpoint and average depth value
    midDepth = depths[int(len(depths) / 2)]
    print(f"Midpoint depth: {midDepth:03f}")
    avgDepth = np.average(depths)
    print(f"Average depth: {avgDepth:03f}")
# end test2()
    
'''
test3()

This test makes a 3D plot of point cloud coordinates. 
'''
def test3(fileNames:list[str], config:CameraLaserConfig, blocking:bool=True, brightnessThreshold:int = 200):
    # Set up 3D points list
    points3d = []
    
    # Loop through all files given
    for fileName in fileNames:
        # Read in image
        frame = cv2.imread(fileName)

        # Fill in config values
        config.xmax = frame.shape[1]
        config.ymax = frame.shape[0]

        # Detect points along the line 
        points2d = detectLine(frame, brightnessThreshold)

        # Calculate depths for each point and convert to 3D point
        for [x, y] in points2d:
            depth = calculateImagePointDepth(x, y, config)
            points3d.append(imageToCameraCoords(x, y, depth, config))
        # end for [x, y]
    # end for fileName

    # Plot points
    plotPointCloud(points3d, blocking)
# end test3()

# Call appropriate tests
if __name__ == "__main__":
    # test1()
    '''
    imageFolder = "test1photos"
    for i in range(8):
        print(f"--- Image {i} ---")
        # test1(f"{imageFolder}\\trial1capture{i:03d}.png", 250)
        test1(f"{imageFolder}\\trial2capture{i:03d}.png", 200)
    '''

    # test2()
    '''
    dlaser = 3.125
    thetaLaser = np.deg2rad(12.5)
    thetaFov = np.deg2rad(55)
    phiLaser = np.deg2rad(90-66.5)
    test2(dlaser, thetaLaser, thetaFov, phiLaser, )
    '''
    '''
    for i in range(8):
        print(f"--- Image {i} ---")
        # test2(dlaser, thetaLaser, thetaFov, phiLaser, f"test1photos\\trial1capture{i:03d}.png", 250)
        test2(dlaser, thetaLaser, thetaFov, phiLaser, f"test1photos\\trial2capture{i:03d}.png", 200)
    '''

    # test3()
    config = CameraLaserConfig(
        None,
        None,
        np.deg2rad(55),
        3.125,
        np.deg2rad(12.5),
        np.deg2rad(90-66.5)
    )

    files = [f"test1photos\\trial1capture{i:03d}.png" for i in range(8)]

    test3(files, config, False)
        
# end if __name__
