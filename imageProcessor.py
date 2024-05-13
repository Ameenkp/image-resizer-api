import cv2


class ImageProcessor:
    def __init__(self, image_width=150, colormap='jet'):
        self.image_width = image_width
        self.colormap = colormap

    def resize_image(self, image):
        return cv2.resize(image, (self.image_width, -1), interpolation=cv2.INTER_AREA)

    def apply_colormap(self, image):
        normalized_image = image.astype(float) / 255.0
        return cv2.applyColorMap(normalized_image, cv2.COLORMAP_[self.colormap])
