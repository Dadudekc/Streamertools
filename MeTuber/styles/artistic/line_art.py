import cv2
import numpy as np
from styles.base import Style

class LineArt(Style):
    """
    A style that applies a line art effect using edge detection.
    """
    name = "Line Art"
    parameters = [
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
        if params is None:
            params = {}
        params = self.validate_params(params)

        threshold1 = params["threshold1"]
        threshold2 = params["threshold2"]

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Canny edge detection
        edges = cv2.Canny(gray, threshold1, threshold2)

        # Invert edges for a line art effect
        line_art = cv2.bitwise_not(edges)

        return line_art
