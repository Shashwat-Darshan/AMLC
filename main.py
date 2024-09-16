import os
import pandas as pd
from tqdm import tqdm
from src.extract_entities import extract_entities_batch

# Enable GPU if available
import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

def process_images(test_df):
    """
    Process all images in the test dataset using the GPU if available.
    """
    total_images = len(test_df)
    results = []

    # Process images one by one
    with tqdm(total=total_images, desc="Processing Images", unit="image") as pbar:
        for i, row in test_df.iterrows():
            image_path = f"./dataset/images/test_image_{row['index']}.jpg"
            entity_name = row['entity_name']

            # Extract entities from the image
            prediction = extract_entities_batch([image_path], device)[0]
            results.append((row['index'], prediction))

            # Update progress bar
            pbar.update(1)

    return results

if __name__ == "__main__":
    DATASET_FOLDER = './dataset/'

    # Load test CSV
    test_df = pd.read_csv(os.path.join(DATASET_FOLDER, 'test.csv'))

    # Process the images and get predictions
    predictions = process_images(test_df)

    # Convert the results back into a DataFrame
    predictions_df = pd.DataFrame(predictions, columns=['index', 'prediction'])

    # Save predictions to test_out.csv
    output_filename = os.path.join(DATASET_FOLDER, 'test_out.csv')
    predictions_df.to_csv(output_filename, index=False)

    print(f"Predictions saved to: {output_filename}")
