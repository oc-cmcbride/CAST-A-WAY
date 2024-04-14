"""
Morgan Demuth adapted from Colin McBride's manualScan.py
Feb 28, 2024
Systems Engineering Design
Team CAST-A-WAY

This program collects image points from pictures.
Generating a 2D point cloud from acquired images.
"""
from MeshGeneration.imageTools import *
from MeshGeneration.capture import Driver
import cv2


class DataCollection:
    def __init__(self):

        self.image_folder = "scan_photos\\"
        self.indexing_file_name = "indexing.txt"

        # Camera parameters
        width = 720
        height = 1280
        horizontal_fov = 30.9375
        print("Acquiring camera resource...")
        self.cap = cv2.VideoCapture(1)
        print("Setting camera width...")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)       # Hardcoding to avoid ambiguity 
        print("Setting camera height...")
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)     # Hardcoding to avoid ambiguity 
        print("Set camera settings!")

        # laser parameters
        dist_laser = 1.539
        theta_laser = 20.775
        phi_laser = 25

        # image parameters
        self.bright_thresh = 250
        self.index_picture = 0
        self.image_name = 'capture'

        # physical configuration parameters 
        self.deg_per_step = 360 / 200
        self.downward_camera_angle = 49     # how many degrees the camera is looking downard into the socket

        # Set up camera/laser config data
        self.clConfig = CameraLaserConfig(
            width,
            height,
            np.deg2rad(horizontal_fov),
            dist_laser,
            np.deg2rad(theta_laser),
            np.deg2rad(phi_laser)
        )
        self.points3d = []
        # Initialize 3D points list
        # This list contains 3-element tuples

    def get_data(self):
        self.get_images()
        self.get_image_points()
        return self.points3d

    def get_images(self):
        # Clear indexing file 
        open(self.indexing_file_name, 'w').close()
        # Runs the motor turning with image taking
        driver = Driver()
        scan = True
        rotate = True
        while scan:
            driver.move_to_start()
            while not driver.rot_sensor:
                driver.rotate_left()
                driver.check_sensors()
                self.get_image()
                with open(self.indexing_file_name, 'a') as f:
                    f.write(f'{self.index_picture - 1},{driver.position[0]},{driver.position[1]},{driver.position[0]*driver.step_cm[0]},{driver.position[1]*driver.step_cm[1]}\n')
            driver.translate_up()
            scan = driver.check_scan_complete()
        print('get images')

    def get_image(self):
        ret, frame = self.cap.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)   # rotate image since camera is sideways
        if not (frame is None):
            cv2.imwrite(f"{self.image_folder}{self.image_name}{self.index_picture :03d}.png", frame)
            self.index_picture += 1
        print('get_image')

    def get_image_points(self):
        # Read in frames from image files and position data from indexing file 
        frames = []
        image_data = []
        num_images = self.index_picture

        with open(self.indexing_file_name, 'r') as f:
            for i in range(num_images):
                frames.append(cv2.imread(f"{self.image_folder}capture{i:03d}.png"))
                data_entry = f.readline().split(",")
                image_data.append([float(val) for val in data_entry])


        # Keep track of which frame is being scanned
        frame_count = 0

        # Read in points from frames
        print("Processing with the following parameters:")
        print(f"Resolution: {self.clConfig.xmax} x {self.clConfig.ymax}")
        print(f"Camera horizontal FOV: {self.clConfig.thetaFov:.4f} rad")
        print(f"Laser distance: {self.clConfig.dLaser}")
        print(f"Laser rotation: Z-axis: {self.clConfig.thetaLaser:.4f} rad, Y-axis: {self.clConfig.phiLaser:.4f} rad")
        for i in range(len(frames)):
            # Get frame and associated data
            frame = frames[i]
            frameData = image_data[i]

            # Calculate new points
            points2d = detectLine(frame, self.bright_thresh)

            # Down-sample the detected points to improve mesh generation
            points2d = points2d[::10]

            # Convert 2d image points to 3d points
            for [x, y] in points2d:
                depth = calculateImagePointDepth(x, y, self.clConfig)
                new_point = imageToCameraCoords(x, y, depth, self.clConfig)

                # Calculate angles 
                alpha = np.deg2rad(self.downward_camera_angle)
                gamma = np.deg2rad(frameData[3] * self.deg_per_step)

                # Generate arrays for multiplication
                Pcc = [ # Point Camera Coordinate
                    [new_point[0]],
                    [new_point[1]],
                    [new_point[2]]
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
                new_point = [p[0] for p in Pwc]

                # Apply vertical offset
                new_point[1] += frameData[4]

                # Add to point list
                self.points3d.append(new_point)
            # end for [x,y] in points2d

            # Increment frame count
            frame_count += 1
        # end for frame in frames
