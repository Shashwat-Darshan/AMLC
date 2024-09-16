# src/download_images.py

import os
import urllib.request
from tqdm import tqdm
from pathlib import Path
from PIL import Image

# Create a placeholder image if download fails
def create_placeholder_image(image_save_path):
    try:
        placeholder_image = Image.new('RGB', (100, 100), color='black')
        placeholder_image.save(image_save_path)
    except Exception as e:
        print(f"Error creating placeholder image: {e}")

# Download an image from a link and save it with a custom name
def download_image(image_link, save_folder, filename, retries=3, delay=3):
    if not isinstance(image_link, str):
        return

    image_save_path = os.path.join(save_folder, filename)

    if os.path.exists(image_save_path):
        return

    for _ in range(retries):
        try:
            urllib.request.urlretrieve(image_link, image_save_path)
            return
        except Exception as e:
            print(f"Error downloading image: {e}")

    # Create a placeholder if download fails after retries
    create_placeholder_image(image_save_path)

# Download images from the list of URLs and save them with the provided custom names
def download_images(image_links, indexes, download_folder):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    for image_link, index in tqdm(zip(image_links, indexes), total=len(image_links)):
        filename = f"test_image_{index}.jpg"  # Custom filename format
        download_image(image_link, save_folder=download_folder, filename=filename)
