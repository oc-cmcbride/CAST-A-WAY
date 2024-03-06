'''
takePic.py

Colin McBride
Oct 13, 2023
Systems Engineering Design
Team CAST-A-WAY

This short program takes a series of pictures using the OpenCV library 
and saves them to the working directory. 
'''
import cv2

# Constants
IMG_NAME = "capture"    # The name to use for captured image. Name format is [IMG_NAME][Image_Index].png
WIDTH = 1280
HEIGHT = 720

# Initialization
running = True              # A boolean to control the main loop
indxPicture = 0             # An integer recording the index of the current image 
print("Acquiring camera resource...")
cap = cv2.VideoCapture(1)   # A video capture object associated with the camera
print("Camera resource acquired!")

# Set capture resolution
print("Setting camera width...")
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
print("Setting camera height...")
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
print("Camera resolution set!")

# Main loop
print("Press \'space\' to take a picture.")
print("Press \'q\' to quit.")
while running:
    # Capture and display current image
    ret, frame = cap.read()
    if not (frame is None):
        cv2.imshow("Window", frame)

    # Wait for spacebar press to capture image, or q to quit
    key = cv2.waitKey(1)
    if (key & 0xFF) == ord(' '):
        # Save current frame
        cv2.imwrite(f"{IMG_NAME}{indxPicture:03d}.png", frame)
        print(f"Saved image \'{IMG_NAME}{indxPicture:03d}.png\'")

        # Increment picture index
        indxPicture = indxPicture + 1
    elif (key & 0xFF) == ord('q'):
        # Quit
        running = False
# end while running

# Deinitialization
cap.release()
cv2.destroyAllWindows()

