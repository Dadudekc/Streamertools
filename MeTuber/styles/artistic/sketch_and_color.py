# File: styles/artistic/sketch_and_color.py

import cv2
import numpy as np
from styles.base import Style


class SketchAndColor(Style):
    """
    A style that combines a pencil sketch effect with color blending.
    """
    name = "Sketch & Color"
    category = "Artistic"
    parameters = [
        {
            "name": "blur_intensity",
            "type": "int",
            "default": 21,
            "min": 1,
            "max": 51,
            "step": 2,
            "label": "Blur Intensity",
        },
        {
            "name": "color_strength",
            "type": "float",
            "default": 0.5,
            "min": 0.0,
            "max": 1.0,
            "step": 0.1,
            "label": "Color Strength",
        },
    ]

    def define_parameters(self):
        """
        Returns the parameter definitions for the Sketch & Color effect.
        """
        return self.parameters

    def apply(self, image, params=None):
        """
        Apply the sketch and color effect to the input image.

        Args:
            image (numpy.ndarray): Input BGR image as a NumPy array.
            params (dict, optional): Dictionary of parameters.

        Returns:
            numpy.ndarray: Processed image with sketch and color effect.

        Raises:
            ValueError: If the input image is None or invalid.
        """
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Input image must be a valid NumPy array.")
        if image.ndim != 3 or image.shape[2] != 3:
            raise ValueError("Input must be a 3-channel BGR image.")

        # Validate and sanitize parameters
        params = self.validate_params(params or {})

        blur_intensity = params["blur_intensity"]
        color_strength = params["color_strength"]

        # Ensure blur intensity is odd
        if blur_intensity % 2 == 0:
            blur_intensity += 1

        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Invert the grayscale image
        inverted_gray = cv2.bitwise_not(gray)

        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(inverted_gray, (blur_intensity, blur_intensity), 0)

        # Invert the blurred image
        inverted_blur = cv2.bitwise_not(blurred)

        # Create pencil sketch effect
        sketch = cv2.divide(gray, inverted_blur, scale=256.0)

        # Blend the pencil sketch with the original image
        sketch_and_color = cv2.addWeighted(
            image, color_strength, 
            cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR), 
            1 - color_strength, 
            0
        )

        return sketch_and_color
