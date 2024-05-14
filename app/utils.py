import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.cm as cm
from PIL.Image import Resampling


def resize_image(df, width=150):
    pixel_data = df.drop(columns=['depth']).values
    depth_data = df['depth'].values

    original_width = pixel_data.shape[1]

    resized_images = []
    for row in pixel_data:
        image = row.reshape(1, original_width)
        image_pil = Image.fromarray(image.astype(np.uint8))
        resized_image_pil = image_pil.resize((width, 1), Resampling.BILINEAR)
        resized_image = np.array(resized_image_pil).flatten()
        resized_images.append(resized_image)

    resized_df = pd.DataFrame(resized_images, columns=[f'pixel_{i}' for i in range(width)])
    resized_df.insert(0, 'depth', depth_data)

    return resized_df


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