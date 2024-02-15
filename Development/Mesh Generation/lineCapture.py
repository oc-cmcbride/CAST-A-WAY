'''
lineCapture.py

Morgan Demuth and Colin McBride, adapted from code by Insider Imaging
Oct 18, 2023
Systems Engineering Design
Team CAST-A-WAY

This program reads in an image with a line laser in it and detects the 
pixel locations of the laser within the image. 

The image is read in and the blue and green channels are filtered out, 
leaving only the red channel. Then, a binary threshold is applied to 
filter out only the points above a certain brightness value. After 
that, the average center of all points above the threshold brightness 
in each row of pixels is found, giving the approximate center of the 
laser line in the image. 

Key Assumptions: 
- The input image contains only a single red laser line. 
'''
import cv2
import numpy as np

# Load the image
image = cv2.imread("capture004.png")

# Extract the red channel
red_channel = image[:, :, 2]
cv2.imshow("Redscale", red_channel)
# red_channel = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imshow("Grayscale", red_channel)

# Apply a threshold to detect the laser line
# Adjust the threshold value as needed
threshold_value = 250
# threshold_value = 200
_, binary = cv2.threshold(red_channel, threshold_value, 255, cv2.THRESH_BINARY)
cv2.imshow("Binary Threshold", binary)

# Find the position with the most white pixels (highest brightness) in each row
most_white_points_per_row = []

for y in range(binary.shape[0]):
    row = binary[y, :]
    white_x = np.where(row > 0)[0]

    x = -1
    if len(white_x) > 0:
        x = int(np.mean(white_x))
        most_white_points_per_row.append((x, y))

    # This portion is just to find the vertical center point in the image 
    # If you do not need this functionality, comment it out or delete it 
    if y == int(binary.shape[0] / 2):
        print(f"Middle point coordinate: ({x}, {y})")
        if x > -1:
            cv2.circle(image, (x, y), 5, (255, 0, 255), -1)  # Magenta point at vertical center point


# Calculate the mean position for multiple points
mean_x = int(np.mean([point[0] for point in most_white_points_per_row]))
mean_y = int(np.mean([point[1] for point in most_white_points_per_row]))

kernel_size = (9, 9)
# Apply Gaussian blur to the mean position
smoothed_mean_x = cv2.GaussianBlur(mean_x, kernel_size, 0)
smoothed_mean_y = cv2.GaussianBlur(mean_y, kernel_size, 0)

# Draw the laser line on the original image
for point in most_white_points_per_row:
    cv2.circle(image, point, 1, (255, 0, 0), -1)  # Blue points
    image[point[1], point[0]] = (0, 255, 0)  # Draw a green pixel at the brightest point

# Ensure smoothed_mean_x and smoothed_mean_y are Python integers
smoothed_mean_x = int(smoothed_mean_x[0])
smoothed_mean_y = int(smoothed_mean_y[0])

# Draw the red point
cv2.circle(image, (smoothed_mean_x, smoothed_mean_y), 1, (255, 0, 0), -1)

# Display the image with the detected laser line and smoothed mean point
cv2.imshow("Laser Line Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
