import cv2
import matplotlib
import numpy as np


def resize_image(image_data, original_width=200, new_width=150):
    image = image_data.reshape(1, original_width)
    resized_image = cv2.resize(image, (new_width, 1), interpolation=cv2.INTER_LINEAR)
    return resized_image.flatten()


def apply_colormap(image_array, colour_map='viridis'):
    colormap = matplotlib.colormaps[colour_map]
    reshaped_image = image_array.reshape((1, -1))
    colored_image = colormap(reshaped_image / 255.0)
    return (colored_image[:, :, :3] * 255).astype(np.uint8)
