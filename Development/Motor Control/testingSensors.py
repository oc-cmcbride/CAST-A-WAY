import serial

# Open serial connection
ser = serial.Serial('COM3', 115200)  # Adjust the port and baud rate as needed
ser.close()
while True:
    # Read a line of data from the serial connection
    data = ser.readline().strip().decode()
    print("Received:", data)
# Allow the user to interrupt the program with Ctrl+C

ser.close()

