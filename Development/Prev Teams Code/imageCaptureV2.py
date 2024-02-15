import cv2
import serial
import time
import os

'''
USER PARAMETERS
'''
# Video capture source
cap = cv2.VideoCapture(1)

# Number of steps in a full rotation
stepCount = 200

# Output folder name
outputFolder = "test1Images"



# Open the port - depending on the port the name can look different
# ser = serial.Serial(port = '/dev/cu.usbserial-1460', baudrate = 9600, timeout = 0.1)
ser = serial.Serial(port = 'COM7', baudrate = 9600, timeout = 0.1)

print("port opened")

# Get parameters
ret, frame = cap.read()
dimensions = frame.shape
height = dimensions[0]
width = dimensions[1]

# Wait for the port to open
time.sleep(2)

# Make directory for output photos
if not os.path.exists(os.path.join(os.getcwd(), outputFolder)):
    os.mkdir(outputFolder)

print(f"Camera parameters: {width}x{height}")

cv2.namedWindow("Window")

for i in range(stepCount):
    ret, frame = cap.read()

    # make a backup for display
    displayImage = frame
    
    cv2.imshow("Window", displayImage)
    cv2.imwrite(f"{os.getcwd()}\\{outputFolder}\\step{i:04d}.png", frame)

    ser.write(bytes('s\n', 'utf-8'))

    data = ''
    while data == '':
        data = ser.readline().decode('utf-8')
    print(data, end='')

    # This breaks on 'q' key
    key = cv2.waitKey(100) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()