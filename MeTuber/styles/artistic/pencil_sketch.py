# MeTuber\styles\artistic\pencil_sketch.py

import cv2
import numpy as np
from styles.base import Style  # Adjust the import path as needed


class PencilSketch(Style):
    """
    A style that creates a pencil sketch effect on the image.
    """
    name = "Pencil Sketch"
    category = "Artistic"

    def define_parameters(self):
        """
        Define parameters for the PencilSketch style.

        :return: List of parameter dictionaries.
        """
        return [
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
        if image.ndim != 3 or image.shape[2] != 3:
            raise ValueError("Input must be a 3-channel BGR image.")

        # Initialize params as an empty dictionary if None
        params = params or {}

        # Validate and sanitize parameters
        params = self.validate_params(params)

        # Extract validated blur intensity
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
