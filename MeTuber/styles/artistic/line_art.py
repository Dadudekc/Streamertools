# File: styles/artistic/line_art.py

import cv2
import numpy as np
from styles.base import Style


class LineArt(Style):
    """
    A style that applies a line art effect using edge detection.
    """
    name = "Line Art"
    category = "Artistic"
    parameters = [
        {
            "name": "threshold1",
            "type": "int",
            "default": 50,
            "min": 0,
            "max": 255,
            "step": 1,
            "label": "Threshold 1",
        },
        {
            "name": "threshold2",
            "type": "int",
            "default": 150,
            "min": 0,
            "max": 255,
            "step": 1,
            "label": "Threshold 2",
        },
    ]

    def define_parameters(self):
        """
        Returns the parameter definitions for the Line Art effect.
        """
        return self.parameters

    def apply(self, image, params=None):
        """
        Applies the line art effect to the image using edge detection.

        Args:
            image (numpy.ndarray): Input image in BGR format.
            params (dict, optional): Parameters for the line art effect.

        Returns:
            numpy.ndarray: Line art image.

        Raises:
            ValueError: If the input image is None or invalid.
        """
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Input image must be a valid NumPy array.")
        if image.ndim != 3 or image.shape[2] != 3:
            raise ValueError("Input image must be a 3-channel (BGR) image.")

        # Validate and sanitize parameters
        params = self.validate_params(params or {})

        threshold1 = params["threshold1"]
        threshold2 = params["threshold2"]

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Canny edge detection
        edges = cv2.Canny(gray, threshold1, threshold2)

        # Invert the edges for a line art effect
        line_art = cv2.bitwise_not(edges)

        # Convert single-channel line art to BGR for consistency
        line_art_bgr = cv2.cvtColor(line_art, cv2.COLOR_GRAY2BGR)

        return line_art_bgr
