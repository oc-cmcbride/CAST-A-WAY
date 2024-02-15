'''
cameraLaserConfigDetect.py
Colin McBride
Feb 7, 2024
Systems Engineering Design
Team CAST-A-WAY

This program detects the current camera/laser configuration by taking two images 
at set distances. This procedure assumes the distances in each image are already 
within the nominal operating range of the current configuration. This is 
intended as more of a fine-tuning program for a configuration that has already 
been approximated. 

USE INSTRUCTIONS
1. Mark 2 known distances away from a flat surface like a wall, floor, or desk. 
   Enter the distances into the constants at the beginning of the code. 
  a. Ideally you will already have an idea of the operating range of the 
     current configuration. Set the distances within that range. 
2. Set the camera/laser setup at the first distance marker and start the 
   program. Look at the video feed to ensure the camera is facing the correct 
   direction, then press space to take a photo. 
3. Move the camera/laser setup to the second distance marker. Look at the video 
   feed to ensure the camera is facing the correct direction, then press space 
   to take a photo. 
4. If performed correctly, the program should output to the terminal the 
   detected camera/laser configuration parameters. 
'''
import cv2
import numpy as np
from imageTools import *

'''
CONSTANTS
'''
UNITS = "in"    # Distance units used 
DIST_1 = 6      # Image 1 distance 
DIST_2 = 8      # Image 2 distance

'''
MAIN
'''
def main():
    # Set up video capture 
    cap = setupVideoCapture()
    
# end main

'''
Call main
'''
if __name__ == "__main__":
    main()
