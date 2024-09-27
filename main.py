import numpy as np
from PIL import Image
from tkinter import Tk, Label, Button, filedialog, Canvas
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from tkinter import StringVar

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def get_image_colors(image_path, num_colors=10):
    # Load image
    image = Image.open(image_path)
    image = image.convert("RGB")
    image = image.resize((200, 200))  # Resize for faster processing

    # Convert image to pixel data
    image_array = np.array(image)
    pixels = image_array.reshape((-1, 3))

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)

    # Get the dominant colors and their percentages
    dominant_colors = kmeans.cluster_centers_
    labels = kmeans.labels_

    # Count the frequency of each label
    counts = np.bincount(labels)

    # Sort by most frequent colors
    percentages = counts / len(labels) * 100
    sorted_indices = np.argsort(percentages)[::-1]  # Sort in descending order

    # Get sorted colors and percentages
    sorted_colors = dominant_colors[sorted_indices]
    sorted_percentages = percentages[sorted_indices]

    # Convert colors to hex
    hex_colors = [rgb_to_hex(color) for color in sorted_colors]

    return hex_colors, sorted_percentages

def show_image_colors(image_path):
    # Clear previous content from canvas
    for widget in canvas.winfo_children():
        widget.destroy()

    # Get dominant colors and percentages
    hex_colors, percentages = get_image_colors(image_path)

    # Display the colors, hex codes, and percentages
    for i, color in enumerate(hex_colors):
        # Create a color block
        color_box = Canvas(canvas, width=100, height=100, bg=color)
        color_box.grid(row=0, column=i, padx=5, pady=5)

        # Display percentage
        percentage_label = Label(canvas, text=f'{percentages[i]:.2f}%')
        percentage_label.grid(row=1, column=i)

        # Display hex code
        hex_label = Label(canvas, text=color)
        hex_label.grid(row=2, column=i)

def open_image():
    # Open file dialog to select an image
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if image_path:
        show_image_colors(image_path)

# Setup GUI window
root = Tk()
root.title("Siris Color Extractor")
root.geometry("1200x400")

# Button to open image
open_button = Button(root, text="Open Image", command=open_image)
open_button.pack(pady=20)

# Canvas to display colors and hex codes
canvas = Canvas(root)
canvas.pack()

# Start the GUI event loop
root.mainloop()