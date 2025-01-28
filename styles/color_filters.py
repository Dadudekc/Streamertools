import cv2
import numpy as np
from .base import Style

class InvertColors(Style):
    """
    Gradually inverts the colors of the image based on the alpha parameter.
    """
    name = "Invert Colors"
    category = "color filters"
    parameters = [
        {
            "name": "invert_alpha",
            "type": "float",
            "default": 1.0,
            "min": 0.0,
            "max": 1.0,
            "step": 0.1,
            "label": "Invert Alpha"
        }
    ]

    def apply(self, image, params=None):
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Invalid image provided. Expected a NumPy array.")
        
        if params is None:
            params = {}
        params = self.validate_params(params)

        alpha = params["invert_alpha"]

        # Invert the image
        inverted = cv2.bitwise_not(image)

        # Blend the original and inverted images using alpha
        blended = cv2.addWeighted(image, 1 - alpha, inverted, alpha, 0)
        return blended


class Negative(Style):
    """
    Fully inverts the colors of the image, creating a negative effect.
    """
    name = "Negative"
    category = "color filters"
    parameters = []

    def apply(self, image, params=None):
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Invalid image provided. Expected a NumPy array.")

        return cv2.bitwise_not(image)


class InvertFilter(Style):
    """
    Alias for Negative effect. Fully inverts the colors of the image.
    """
    name = "Invert Filter"
    category = "color filters"
    parameters = []

    def apply(self, image, params=None):
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Invalid image provided. Expected a NumPy array.")

        return cv2.bitwise_not(image)
