import tkinter as tk
import serial

# Initialize the serial port
ser = serial.Serial('COM3', 115200)  # Adjust the port and baud rate as needed

counter = 0


def send_data():
    global counter
    character = 't'  # Character to send
    repetitions = 100000  # Number of times to send the character

    # Send the character the specified number of times
    ser.write((character * repetitions).encode())  # Send the character repeated 50 times as bytes

    # Increment counter
    counter += 1
    print("Counter:", counter)


# Create a simple GUI
root = tk.Tk()
root.title("Serial Port Communication")

# Create a button to send data
button = tk.Button(root, text="Send Data", command=send_data)
button.pack()

root.mainloop()

# Close the serial port when the GUI is closed
ser.close()

