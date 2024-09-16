import re
import os
import requests
from pathlib import Path
from PIL import Image
from tqdm import tqdm
import constants

def common_mistake(unit):
    if unit in constants.allowed_units:
        return unit
    if unit.replace('ter', 'tre') in constants.allowed_units:
        return unit.replace('ter', 'tre')
    if unit.replace('feet', 'foot') in constants.allowed_units:
        return unit.replace('feet', 'foot')
    return unit

def download_image(image_link, save_folder, retries=3, delay=3):
    if not isinstance(image_link, str):
        return

    filename = Path(image_link).name
    image_save_path = os.path.join(save_folder, filename)

    if os.path.exists(image_save_path):
        return

    for _ in range(retries):
        try:
            response = requests.get(image_link)
            if response.status_code == 200:
                with open(image_save_path, 'wb') as f:
                    f.write(response.content)
            return
        except:
            continue
    
    # Create a placeholder image for invalid links/images
    placeholder_image = Image.new('RGB', (100, 100), color='black')
    placeholder_image.save(image_save_path)

def download_images(image_links, download_folder, allow_multiprocessing=True):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    for image_link in tqdm(image_links, total=len(image_links)):
        download_image(image_link, save_folder=download_folder, retries=3, delay=3)
