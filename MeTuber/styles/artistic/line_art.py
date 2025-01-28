import cv2
import numpy as np
from styles.base import Style


class LineArt(Style):
    """
    A style that applies a line art effect using edge detection.
    """
    name = "Line Art"
    category = "Artistic"

    def define_parameters(self):
        """
        Defines the parameters for the Line Art effect.
        """
        return [
            {
                "name": "threshold1",
                "type": "int",
                "default": 50,
                "min": 0,
                "max": 255,
                "step": 1,
                "label": "Threshold 1"
            },
            {
                "name": "threshold2",
                "type": "int",
                "default": 150,
                "min": 0,
                "max": 255,
                "step": 1,
                "label": "Threshold 2"
            }
        ]

    def apply(self, image, params=None):
        """
        Applies the line art effect to the image using edge detection.

        Args:
            image (numpy.ndarray): Input image in BGR format.
            params (dict, optional): Parameters for the line art effect.

        Returns:
            numpy.ndarray: Line art image.
        """
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Input image must be a valid NumPy array.")
        if params is None:
            params = {}

        # Validate and sanitize parameters
        params = self.validate_params(params)

        threshold1 = params["threshold1"]
        threshold2 = params["threshold2"]

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Canny edge detection
        edges = cv2.Canny(gray, threshold1, threshold2)

        # Invert the edges for a line art effect
        line_art = cv2.bitwise_not(edges)

        return line_art
