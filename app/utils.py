import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.cm as cm
from PIL.Image import Resampling
import cv2


def resize_image(image_data, original_width=200, new_width=150):
    # Assuming image_data is a flat array, reshape it to (1, original_width)
    image = image_data.reshape(1, original_width)
    # Resize the image
    resized_image = cv2.resize(image, (new_width, 1), interpolation=cv2.INTER_LINEAR)
    return resized_image.flatten()


def apply_colormap(image_array):
    colormap = cm.get_cmap('viridis')
    # Reshape the image array to the appropriate dimensions
    # Adjust the reshape dimensions according to the actual dimensions of your image
    # For example, if the original image shape is (n_rows, n_columns), reshape to (1, n_rows * n_columns)
    reshaped_image = image_array.reshape((1, -1))
    # Apply the colormap to the reshaped image
    colored_image = colormap(reshaped_image / 255.0)
    # Convert the colored image to uint8 and return
    return (colored_image[:, :, :3] * 255).astype(np.uint8)
