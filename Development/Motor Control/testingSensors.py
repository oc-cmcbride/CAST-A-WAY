import tkinter as tk
import serial

# Function to update sensor status based on received data
def update_sensor_status(data):
    sensor_status.config(text=f"Sensor Status: {data}", bg="green" if data == 1 else "white")


# Function to read data from serial connection
def read_serial():
    try:
        # Read a line of data from the serial connection
        data = int(ser.readline().strip().decode())
        update_sensor_status(data)
    except ValueError:
        pass  # Skip this iteration if the received data is not a valid integer
    root.after(100, read_serial)  # Schedule the next read after 100ms


# Open serial connection
ser = serial.Serial('COM3', 115200)  # Adjust the port and baud rate as needed

# Create the GUI
root = tk.Tk()
root.title("Sensor Display")

sensor_status = tk.Label(root, text="Sensor Status", width=20, height=5, bg="white")
sensor_status.pack()

# Start reading from serial connection
read_serial()

# Start the GUI main loop
root.mainloop()

# Close serial connection
ser.close()


