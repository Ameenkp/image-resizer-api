import os
import numpy as np
import pandas as pd
from PIL import Image


class ImageGenerator:
    def __init__(self, num_images, image_width, image_height, output_dir):
        self.num_images = num_images
        self.image_width = image_width
        self.image_height = image_height
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_image(self):
        img_array = np.random.randint(0, 256, size=(self.image_height, self.image_width, 3), dtype=np.uint8)
        return Image.fromarray(img_array, 'RGB')

    def generate_and_save_image(self, depth):
        image = self.generate_image()
        image_path = os.path.join(self.output_dir, f"image_{depth}.png")
        image.save(image_path)
        return image_path


class DatasetGenerator:
    def __init__(self, img_generator):
        self.image_generator = img_generator

    def generate_dataset(self):
        img_data = []
        for depth in range(1, self.image_generator.num_images + 1):
            image_path = self.image_generator.generate_and_save_image(depth)
            image = Image.open(image_path)
            pixels = np.array(image).flatten()
            img_data.append([depth] + pixels.tolist())
            print(f"Image {depth} generated and saved at {image_path}")
        return img_data


# Constants
NUM_IMAGES = 100
IMAGE_WIDTH = 200
IMAGE_HEIGHT = 150
OUTPUT_DIR = "generated_images"

# Create ImageGenerator instance
image_generator = ImageGenerator(NUM_IMAGES, IMAGE_WIDTH, IMAGE_HEIGHT, OUTPUT_DIR)

# Create DatasetGenerator instance
dataset_generator = DatasetGenerator(image_generator)

# Generate dataset
image_data = dataset_generator.generate_dataset()

# Convert to DataFrame
columns = ['depth'] + [f'pixel_{i}' for i in range(IMAGE_WIDTH * IMAGE_HEIGHT * 3)]
df = pd.DataFrame(image_data, columns=columns)

# Save DataFrame to CSV
csv_file = 'sample_dataset.csv'
df.to_csv(csv_file, index=False)

print(f"Dataset saved as {csv_file}")
