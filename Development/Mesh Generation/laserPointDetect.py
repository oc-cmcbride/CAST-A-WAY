'''
laserPointDetect.py

Colin McBride, adapted from code by Noah Doner from Insider Imaging
Oct 11, 2023
Systems Engineering Design
Team CAST-A-WAY

This program reads in an image with a line laser in it and detects the 
pixel locations of the laser within the image. 

The detection algorithm breaks the image into horizontal strips, and each 
strip is scanned for the brightest point. The x coordinate of the 
point is determined by the brightest point in the strip. The y coordinate 
is determined by the strip location. 
'''
import cv2
import numpy as np

'''
CONSTANTS
'''
imgPath = 'capture004.png'    # Path to the image to scan
brad = 21                   # Blur radius for the Gaussion blur - must be odd
stripHeight = 10            # Height of horizontal strips, in pixels 
brightnessThreshold = 120   # Brightness threshold to detect a point in a strip 


'''
READ IMAGE TO SCAN
'''
frame = cv2.imread(imgPath)

# Get height and width of image 
height = frame.shape[0]
width = frame.shape[1]

# Calculate strip count based on image height 
stripCount = int(height / stripHeight)

'''
DETECT LASER ON IMAGE
'''
# make a backup for display
displayImage = frame

# Separate color channels to get red because eevee rendering no realistic
(B, G, R) = cv2.split(frame)
# Blur to reduce noise
gray = cv2.GaussianBlur(R, (brad, 1), 0)

cameraPoints = [None] * stripCount

for i in range(stripCount):
    # crop to strip - numpy does rows and columns instead of x and y because ¯\_(ツ)_/¯
    strip = gray[stripHeight * i : stripHeight * (i + 1), :]
    
    # decimate y axis
    strip = cv2.resize(strip, (width, 1), interpolation = cv2.INTER_AREA)

    # Find brightest point
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(strip)
    # print(f"location: {str(maxLoc)}\tvalue: {maxVal}")

    xLoc = maxLoc[0]

    if(maxVal > brightnessThreshold):
        cameraPoints[i] = (float(xLoc), stripHeight * (i + 0.5))
        displayImage = cv2.circle(frame, [round(cameraPoints[i][0]), round(cameraPoints[i][1])], 3, (100, 255, 100), -1)


# Remove Nones
uvPoints = np.array(list(filter(lambda item: item is not None, cameraPoints)))
# Normalize coordinates
uvPoints[:, 0] = 2 * uvPoints[:, 0] / width - 1
uvPoints[:, 1] = 2 * uvPoints[:, 1] / height - 1

'''
OUTPUT RESULTS
'''
# Find center index
centerIndex = int(len(cameraPoints) / 2)

# Mark center point on image
displayImage = cv2.circle(frame, [round(cameraPoints[centerIndex][0]), round(cameraPoints[centerIndex][1])], 3, (255, 100, 100), -1)

# Print results
print(f"Image dimensions: ({width}px, {height}px)")
print(f"Coordinate of center strip: ({cameraPoints[centerIndex][0]}px, {cameraPoints[centerIndex][1]}px)")


# Show image. Press q to quit. 
cv2.imshow("Window", displayImage)
print("Press any key to quit.")
cv2.waitKey(0)
