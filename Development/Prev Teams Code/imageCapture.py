import cv2
import serial
import time

# Open the port - depending on the port name can look a lot different
ser = serial.Serial(port = '/dev/cu.usbserial-1460', baudrate = 9600, timeout = 0.1)

print("port opened")

# Get the video capture
cap = cv2.VideoCapture(1)

stepCount = 200

# Get parameters
ret, frame = cap.read()
dimensions = frame.shape
height = dimensions[0]
width = dimensions[1]

# Wait for the port to open
time.sleep(2)

print(f"Camera parameters: {width}x{height}")

cv2.namedWindow("Window")

for i in range(stepCount):
    ret, frame = cap.read()

    # make a backup for display
    displayImage = frame;
    
    cv2.imshow("Window", displayImage)
    cv2.imwrite(f"step{i:04d}.png", frame)

    ser.write(bytes('s\n', 'utf-8'))

    data = ''
    while data == '':
        data = ser.readline().decode('utf-8')
    print(data, end='')

    # This breaks on 'q' key
    key = cv2.waitKey(100) & 0xFF;
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()