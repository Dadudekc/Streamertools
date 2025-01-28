import cv2
import numpy as np
from styles.base import Style

class InvertFilter(Style):
    """
    Alias for Negative effect. Fully inverts the colors of the image.
    """
    name = "Invert Filter"
    category = "color filters"

    def define_parameters(self):
        return []

    def apply(self, image, params=None):
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Invalid image provided. Expected a NumPy array.")

        return cv2.bitwise_not(image)
