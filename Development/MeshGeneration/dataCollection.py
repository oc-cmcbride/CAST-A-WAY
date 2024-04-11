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

        self.image_folder = "test1photos\\"

        # Camera parameters
        width = 1280
        height = 720
        horizontal_fov = 55
        self.cap = cv2.VideoCapture(1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        # laser parameters
        dist_laser = 3.125
        theta_laser = 12.5
        phi_laser = 90 - 66.5

        # image parameters
        self.bright_thresh = 200
        self.index_picture = 0
        #                    X, Y, Z
        self.point_offset = [1, 0, 0]
        self.image_name = 'capture'

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
        driver = Driver()
        scan = True
        rotate = True
        while scan:
            driver.move_to_start()
            while not driver.rot_sensor:
                self.get_image()
                driver.rotate_left()
                driver.check_sensors()
            driver.translate_up()
            scan = driver.check_scan_complete()
        print('get images')

    def get_image(self):
        # ret, frame = self.cap.read()
        # if not (frame is None):
        #     cv2.imwrite(f"{self.image_name}{index_picture:03d}.png", frame)
        #     self.index_picture += 1
        print('get_image')

    def get_image_points(self):
        # Read in frames from image files
        frames = []
        num_images = self.index_picture

        for i in range(num_images):
            frames.append(cv2.imread(f"{self.image_folder}capture{i:03d}.png"))

        # Keep track of which frame is being scanned
        frame_count = 0

        # Read in points from frames
        print("Processing with the following parameters:")
        print(f"Resolution: {self.clConfig.xmax} x {self.clConfig.ymax}")
        print(f"Camera horizontal FOV: {self.clConfig.thetaFov:.4f} rad")
        print(f"Laser distance: {self.clConfig.dLaser}")
        print(f"Laser rotation: Z-axis: {self.clConfig.thetaLaser:.4f} rad, Y-axis: {self.clConfig.phiLaser:.4f} rad")
        for frame in frames:
            # Calculate new points
            points2d = detectLine(frame, self.bright_thresh)

            # Down-sample the detected points to improve mesh generation
            points2d = points2d[::10]

            # Convert 2d image points to 3d points
            for [x, y] in points2d:
                depth = calculateImagePointDepth(x, y, self.clConfig)
                new_point = imageToCameraCoords(x, y, depth, self.clConfig)

                # Apply offset
                new_point[0] += self.point_offset[0] * frame_count
                new_point[1] += self.point_offset[1] * frame_count
                new_point[2] += self.point_offset[2] * frame_count

                # Add to point list
                self.points3d.append(new_point)
            # end for [x,y] in points2d

            # Increment frame count
            frame_count += 1
        # end for frame in frames
