'''
cameraLaserConfigDetect.py
Colin McBride
Feb 28, 2024
Systems Engineering Design
Team CAST-A-WAY

This program detects the current camera/laser configuration by taking N number 
of  images at set distances. This procedure assumes the distances in each image 
are already within the nominal operating range of the current configuration. 
This is intended as more of a fine-tuning program for a configuration that has 
already been approximated. 

USE INSTRUCTIONS
1. Mark N known distances away from a flat surface like a wall, floor, or desk. 
   Enter the distances into the constants at the beginning of the code. 
  a. Ideally you will already have an idea of the operating range of the 
     current configuration. Set the distances within that range. 
2. Set the camera/laser setup at the first distance marker and start the 
   program. Look at the video feed to ensure the camera is facing the correct 
   direction, then press space to take a photo. 
3. Move the camera/laser setup to the next distance marker. Look at the video 
   feed to ensure the camera is facing the correct direction, then press space 
   to take a photo. 
4. Repeat step 3 for all N distances. 
5. If performed correctly, the program should output to the terminal the 
   detected camera/laser configuration parameters. 
'''
import cv2
import numpy as np
from imageTools import *

'''
CONSTANTS
'''
UNITS = "in"    # Distance units used 
DISTANCES = [     # Array with distance values. The length of this array determines how many pictures will be taken. 
   2.5444,
   2.9224,
   3.3004,
   3.6784,
   4.0564,
   4.4344
]
HFOV = 30.9375          # Horizontal FOV of the camera (degrees)

'''
estimatePhiLaser()
Takes in a set of laser points that have already been extracted from an image 
and returns the angle of the line in the image.
!!! Note this assumes that there is NO CHANGE IN DEPTH in the image !!!
'''
def estimatePhiLaser(points, inDeg:bool=False):
   # Transpose points list
   transPoints = list(zip(*points))

   # Calculate best fit line
   m, b = np.polyfit(transPoints[0], transPoints[1], 1)

   # Calculate angle of laser from best fit line 
   angle = (np.pi / 2) - np.arctan(m)
   if inDeg:
      angle = np.rad2deg(angle)
   
   # Return results
   return angle
# end estimatePhiLaser

'''
estimateConfiguration()
Takes in a set of images and their respective distances and outputs the camera 
configuration estimate from the images. 
'''
def estimateConfiguration(
   image1:np.ndarray, 
   dist1:float, 
   image2:np.ndarray, 
   dist2:np.ndarray,
   thetaFov:float
) -> CameraLaserConfig:
   # Create config struct
   config = CameraLaserConfig(
      xmax = image1.shape[1],
      ymax = image1.shape[0],
      thetaFov = thetaFov,
      dLaser = None,
      thetaLaser = None,
      phiLaser = None
   )

   # Get laser points from images
   img1points = detectLine(image1, 250)
   img2points = detectLine(image2, 250)

   # Average phiLaser of both images
   config.phiLaser = (estimatePhiLaser(img1points) + estimatePhiLaser(img2points)) / 2

   # Create result lists
   dLaserPoints = []
   thetaLaserPoints = []

   # Loop through all points in the images
   for (x1, y1) in img1points:
      # Extract points
      y2 = y1
      x2 = img2points[y2][0]

      # Create coefficient matrices
      a = np.array([
         [1, -dist1],
         [1, -dist2]
      ])
      b = np.array([
         [dist1 * np.tan(thetaFov * ((x1 - ((y1 - 0.5*config.ymax) * np.tan(config.phiLaser))) / config.xmax - 0.5))],
         [dist2 * np.tan(thetaFov * ((x2 - ((y2 - 0.5*config.ymax) * np.tan(config.phiLaser))) / config.xmax - 0.5))]
      ])

      # Solve for dLaser and thetaLaser
      result = np.linalg.solve(a, b)
      dLaserPoints.append(result[0][0])
      thetaLaserPoints.append(np.arctan(result[1][0]))
   # end for (x,y)
      
   # Average points for final result
   config.dLaser = np.average(dLaserPoints)
   config.thetaLaser = np.average(thetaLaserPoints)

   # Return resulting configuration
   return config
# end estimateConfiguratino

'''
MAIN
'''
def main():
   
   # Initialization
   numImages = len(DISTANCES)
   picsRemaining = len(DISTANCES)
   images = []

   # Set up video capture 
   cap = setupVideoCapture(verbose=True)
   
   # Start camera loop
   print("Press \'space\' to take a picture. \nPress \'q\' to quit.")
   while picsRemaining > 0:
      # Capture and display current image 
      ret, frame = cap.read()
      frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)   # Rotate image because camera is rotated
      if not ret:
         print("ERROR: Webcam could not display frame!")
         break
      cv2.imshow("Camera Output", frame)

      # Wait for keystrokes
      key = cv2.waitKey(1)
      if (key & 0xFF) == ord(' '):
         # Save current frame
         if picsRemaining > 0:
            # cv2.imwrite(f"configCapture{numImages - picsRemaining}.png")
            images.append(frame.copy())
            picsRemaining -= 1
            print(f"Image {numImages - picsRemaining} of {numImages} captured!")
      elif (key & 0xFF) == ord('q'):
         # Quit
         break
   # end while picsRemaining > 0
   
   # Process images (if all were captured)
   if picsRemaining == 0:
      # Perform all possible permutations
      dLaserPoints = []
      thetaLaserPoints = []
      phiLaserPoints = []
      for i in range(numImages):
         for j in range(i + 1, numImages):
            config = estimateConfiguration(images[i], DISTANCES[i], images[j], DISTANCES[j], np.deg2rad(HFOV))
            dLaserPoints.append(config.dLaser)
            thetaLaserPoints.append(config.thetaLaser)
            phiLaserPoints.append(config.phiLaser)
      
      # Average results from all 
      dLaser = np.average(dLaserPoints)
      thetaLaser = np.average(thetaLaserPoints)
      phiLaser = np.average(phiLaserPoints)
      print(f"dLaser: {dLaser} {UNITS}, thetaLaser: {np.rad2deg(thetaLaser)} deg, phiLaser: {np.rad2deg(phiLaser)} deg")
      print(f"Config values: {config}")
   else:
      print("ERROR: Not enough input images captured.")
   # end if picsRemaining == 0
# end main

'''
Call main
'''
if __name__ == "__main__":
   main()