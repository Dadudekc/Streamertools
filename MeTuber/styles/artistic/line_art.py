# File: styles/artistic/line_art.py

import cv2
import numpy as np
from styles.base import Style


class LineArt(Style):
    """
    A style that applies a line art effect using edge detection.
    """
    def __init__(self):
        super().__init__()
        self.name = "Line Art"
        self.category = "Artistic"

    def define_parameters(self):
        """
        Define parameters for line art effect.
        """
        return {
            "threshold1": {"default": 50, "min": 0, "max": 255},
            "threshold2": {"default": 150, "min": 0, "max": 255},
            "aperture_size": {"default": 3, "min": 3, "max": 7, "step": 2}
        }

    def apply(self, image, params=None):
        """
        Apply line art effect to the image.
        
        Args:
            image (numpy.ndarray): Input image in BGR format
            params (dict, optional): Parameters for the effect
                - threshold1: First threshold for edge detection
                - threshold2: Second threshold for edge detection
                - aperture_size: Aperture size for the Sobel operator
        
        Returns:
            numpy.ndarray: Image with line art effect in grayscale format
        """
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Input image must be a valid NumPy array")

        # Use default parameters if none provided
        if params is None:
            params = {name: param["default"] for name, param in self.define_parameters().items()}

        # Get and validate parameters
        t1 = params.get("threshold1", 50)
        if not 0 <= t1 <= 255:
            raise ValueError("Parameter 'threshold1' must be between 0 and 255.")

        t2 = params.get("threshold2", 150)
        if not 0 <= t2 <= 255:
            raise ValueError("Parameter 'threshold2' must be between 0 and 255.")

        aperture = params.get("aperture_size", 3)
        if aperture not in [3, 5, 7]:
            raise ValueError("Parameter 'aperture_size' must be 3, 5, or 7.")

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply edge detection
        edges = cv2.Canny(gray, t1, t2, apertureSize=aperture)

        # Invert the edges to get white lines on black background
        return cv2.bitwise_not(edges)
