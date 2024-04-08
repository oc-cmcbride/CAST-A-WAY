import serial
import tkinter as tk

# Initialize serial port
ser = serial.Serial('COM3', 115200)  # Change 'COM1' to the appropriate port and 9600 to the baud rate of your device
ser.close()
counter = 0


def send_data():
    global counter
    character = 't'  # Character to send
    repetitions = 50  # Number of times to send the character

    # Send the character the specified number of times
    ser.write((character * repetitions).encode())  # Send the character repeated 10 times as bytes

    # Increment counter
    counter += 1
    print("Counter:", counter)


# Create a simple GUI
root = tk.Tk()
root.title("Serial Port Communication")

counter_label = tk.Label(root, text="Counter: 0")
counter_label.pack()

button = tk.Button(root, text="Send Character", command=send_data)
button.pack(pady=20)

root.mainloop()

ser.close()
