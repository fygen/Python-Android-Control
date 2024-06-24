import tkinter as tk
from tkinter import messagebox
from ppadb.client import Client

def getADBDevice():
    adb = Client (host='127.0.0.1',port=5037 )
    devices = adb.devices()
    if len(devices) == 0:
        print ('no device attached')
        return 'no device attached'
    print( str(devices[0]))
    return devices[0]

# Function to handle button click
def greet():
    messagebox.showinfo("Hello", f"Hello, {user_name.get()}!")

def divAndSend():
    xStart,xEnd,yStart,yEnd = user_name.get().split(" ")
    swipeScreen(device,xStart,xEnd,yStart,yEnd, 1000)


def swipeScreen(device,xStart,xEnd,yStart,yEnd, distance):
    device.shell(f'input touchscreen swipe {xStart} {xEnd} {yStart} {yEnd} {int(distance)}')

# Create the main window
root = tk.Tk()
device = getADBDevice()
root.title(device) # TITLE IS HERE

# Create a label
label = tk.Label(root, text="Enter xStart xEnd yStart yEnd:")
label.pack(pady=10)

# Create an entry widget
user_name = tk.StringVar()
entry = tk.Entry(root, textvariable=user_name)
entry.pack(pady=5)

ent = tk.Text(root,pady=10)

# Create a button
button = tk.Button(root, text="Greet", command=greet)
button.pack(pady=10)

button2 = tk.Button(root, text="Swipe Screen",command=divAndSend)
button2.pack(pady=10)

# Run the main loop
root.mainloop()