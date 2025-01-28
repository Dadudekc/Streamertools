# styles/artistic/pencil_sketch.py

import cv2
import numpy as np  # Ensure numpy is imported
from styles.base import Style  # Use absolute import


class PencilSketch(Style):
    """
    A style that creates a pencil sketch effect on the image.
    """
    name = "Pencil Sketch"
    category = "Artistic Styles"
    parameters = [
        {
            "name": "blur_intensity",
            "type": "int",
            "default": 21,
            "min": 1,
            "max": 51,
            "step": 2,
            "label": "Blur Intensity"
        }
    ]

    def apply(self, image, params=None):
        """
        Apply the pencil sketch effect using the validated parameters.
        
        :param image: Input BGR image as a NumPy array.
        :param params: Dictionary of parameters.
        :return: Processed image with pencil sketch effect.
        :raises ValueError: If the input image is None or invalid.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")
        if not isinstance(image, np.ndarray):
            raise ValueError("Input must be a valid NumPy array.")

        # Initialize params as an empty dictionary if None
        params = params or {}

        # Validate and sanitize parameters
        params = self.validate_params(params)

        blur_intensity = params["blur_intensity"]

        # Ensure blur intensity is odd
        if blur_intensity % 2 == 0:
            blur_intensity += 1

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Invert the grayscale image
        inverted_gray = cv2.bitwise_not(gray)

        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(inverted_gray, (blur_intensity, blur_intensity), 0)

        # Invert the blurred image
        inverted_blur = cv2.bitwise_not(blurred)

        # Divide gray by the inverted blur to create a sketch effect
        sketch = cv2.divide(gray, inverted_blur, scale=256.0)

        return sketch
