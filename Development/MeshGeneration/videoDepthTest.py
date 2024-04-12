'''
videoDepthTest.py
Colin McBride
Jan 25, 2024
Systems Engineering Design
Team CAST-A-WAY

This program scans images from a video feed and dynamically outputs 
3D coordinate estimations on a 3D plot. 
'''
import numpy as np
from imageTools import *

'''
CONSTANTS
'''
WIDTH = 720
HEIGHT = 1280
H_FOV = 30.9375
D_LASER = 1.539
THETA_LASER = 20.775
PHI_LASER = 25
BRIGHT_THRESH = 250

'''
MAIN
'''
if __name__ == "__main__":
    # Create video capture object
    cap = setupVideoCapture(1, verbose=True)

    # Create plot
    fig = plt.figure()
    ax = plt.axes(projection="3d")
    plt.ion()
    plt.show()

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
    points3d = []

    # Main loop
    print("Scanning with the following parameters:")
    print(f"Resolution: {clConfig.xmax} x {clConfig.ymax}")
    print(f"Camera horizontal FOV: {clConfig.thetaFov:.4f} rad")
    print(f"Laser distance: {clConfig.dLaser}")
    print(f"Laser rotation: Z-axis: {clConfig.thetaLaser:.4f} rad, Y-axis: {clConfig.phiLaser:.4f} rad")
    running = True
    while running:
        # Capture and display current image 
        ret, frame = cap.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)   # Rotate image since camera is rotated
        if not (frame is None):
            cv2.imshow("Camera", frame)

            # Calculate new points
            points3d.clear()
            points2d = detectLine(frame, BRIGHT_THRESH)
            for [x, y] in points2d:
                depth = calculateImagePointDepth(x, y, clConfig)
                points3d.append(imageToCameraCoords(x, y, depth, clConfig))
            
            # Check if any points were found
            if len(points3d) > 0:
                # Transpose data
                [x, y, z] = list(zip(*points3d))

                # Plot points
                plt.cla()
                ax.scatter(x, y, z)
                plt.pause(0.01)
            # end if len(points3d)
        # end if not (frame is None)

        # Check for quit condition
        key = cv2.waitKey(1)
        if (key & 0xFF) == ord('q'):
            # Quit
            running = False
    # end while running
            
    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    plt.close()
# end if __name__