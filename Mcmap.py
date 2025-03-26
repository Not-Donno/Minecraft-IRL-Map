import tkinter as tk
from tkinter import ttk
import folium
import geocoder
import os
import random
import webview
from PIL import Image, ImageDraw

def get_current_location():
    g = geocoder.ip('me')
    return g.latlng

BLOCK_TYPES = ["grass", "dirt", "stone"]


def generate_block_image(width=32, height=32):
    block_type = random.choice(BLOCK_TYPES)
    
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    if block_type == "grass":
        draw.rectangle([0, 0, width, height], fill=(87, 166, 41)) 
    elif block_type == "dirt":
        draw.rectangle([0, 0, width, height], fill=(155, 118, 83)) 
    elif block_type == "stone":
        draw.rectangle([0, 0, width, height], fill=(169, 169, 169))  

    return img

def generate_grid(width=800, height=600, block_size=32):
    grid_width = width // block_size
    grid_height = height // block_size
    grid_img = Image.new('RGB', (width, height))
    for i in range(grid_width):
        for j in range(grid_height):
            block_img = generate_block_image(block_size, block_size)
            grid_img.paste(block_img, (i * block_size, j * block_size))

    return grid_img
def create_map():
    location = get_current_location()

    if location:
        latitude, longitude = location
    else:
        latitude, longitude = 51.5074, -0.1278

    map_img = generate_grid()

    map_image_path = 'minecraft_map.png'
    map_img.save(map_image_path)
    m = folium.Map(location=[latitude, longitude], zoom_start=12)
    m_html = f"""
    <html>
    <body style="margin:0;padding:0;">
        <img src="file:///{os.path.abspath(map_image_path)}" width="100%" height="100%">
    </body>
    </html>
    """
    map_file = 'map.html'
    with open(map_file, 'w') as f:
        f.write(m_html)

    abs_map_file = os.path.abspath(map_file)
    return abs_map_file, map_image_path

def create_ui():
    window = tk.Tk()
    window.title("Minecraft Style Map Viewer")
    window.geometry("800x600")

    frame = ttk.Frame(window)
    frame.pack(fill=tk.BOTH, expand=True)

    map_file, block_image_path = create_map()

    webview.create_window("Minecraft Style Map Viewer", f"file:///{map_file}")
    webview.start()

create_ui()
