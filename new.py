
# run this command. 
# pip install opencv-python-headless Pillow


import cv2
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import time

# Function to update the webcam feed
def update_frame():
    global last_frame_time
    current_time = time.time() * 1000  # current time in milliseconds
    if current_time - last_frame_time >= frame_delay:
        ret, frame = cap.read()
        if ret:
            # Resize the frame to fit the window
            frame = cv2.resize(frame, (frame_width, frame_height))
            # Convert the frame to RGB format
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
        last_frame_time = current_time
    lmain.after(10, update_frame)

# Create the main window
root = tk.Tk()
root.title("Floating Webcam")
root.attributes("-topmost", True)  # Keep the window on top
root.geometry("320x240")  # Initial window size

# Remove window decorations
root.overrideredirect(True)

# Open the webcam
cap = cv2.VideoCapture(0)

# Set the desired frame rate
desired_fps = 10
frame_delay = int(1000 / desired_fps)  # delay between frames in milliseconds
last_frame_time = 0

# Set the desired frame width and height (lower resolution)
frame_width = 320
frame_height = 240
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

# Create a label to display the webcam feed
lmain = Label(root)
lmain.pack(fill=tk.BOTH, expand=True)  # Make the label expand to fit the window

# Start updating the frame
update_frame()

# Function to handle dragging of the window
def start_move(event):
    global x, y
    x = event.x
    y = event.y

def do_move(event):
    deltax = event.x - x
    deltay = event.y - y
    root.geometry(f"+{root.winfo_x() + deltax}+{root.winfo_y() + deltay}")

# Bind mouse events to handle window dragging
lmain.bind("<Button-1>", start_move)
lmain.bind("<B1-Motion>", do_move)

# Run the main loop
root.mainloop()

# Release the webcam when the window is closed
cap.release()
cv2.destroyAllWindows()
