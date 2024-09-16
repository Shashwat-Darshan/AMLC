import easyocr
import os
import torch
from src.preprocess_ocr import preprocess_image

# Initialize EasyOCR with GPU support if available
device = "cuda" if torch.cuda.is_available() else "cpu"
reader = easyocr.Reader(['en'], gpu=torch.cuda.is_available())

def extract_entities_batch(image_paths, device="cpu"):
    """
    Process a batch of images using EasyOCR on the GPU if available.
    """
    batch_results = []
    for image_path in image_paths:
        if not os.path.exists(image_path):
            batch_results.append("")
            continue

        try:
            # Preprocess the image
            preprocessed_image = preprocess_image(image_path)

            # Perform OCR on the image
            result = reader.readtext(preprocessed_image)

            # Extract the text and entities
            extracted_text = " ".join([item[1] for item in result])
            batch_results.append(extracted_text)

        except Exception as e:
            batch_results.append("")

    return batch_results
