import cv2
import numpy as np

def preprocess_image(image_path, target_size=(512, 512)):
    """
    Preprocess the image by resizing and applying grayscale and thresholding.
    """
    image = cv2.imread(image_path)

    # Resize the image to reduce processing time
    image = cv2.resize(image, target_size)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive thresholding to improve text extraction
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    return thresh
