# styles\basic\color_balance.py

import cv2
import numpy as np
from ..base import Style

class ColorBalance(Style):
    """
    Adjusts the color balance of the image by shifting blue, green, and red channels.
    """
    name = "Color Balance"
    category = "Basic"
    parameters = [
        {"name": "blue_shift", "type": "int", "default": 0, "min": -50, "max": 50, "step": 1, "label": "Blue Shift"},
        {"name": "green_shift", "type": "int", "default": 0, "min": -50, "max": 50, "step": 1, "label": "Green Shift"},
        {"name": "red_shift", "type": "int", "default": 0, "min": -50, "max": 50, "step": 1, "label": "Red Shift"},
    ]

    def apply(self, image, params=None):
        """
        Applies color balance adjustments to the image.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")

        # Initialize params if None
        params = params or {}

        # Validate and sanitize parameters
        params = self.validate_params(params)

        # Extract channel shift values
        blue_shift = params["blue_shift"]
        green_shift = params["green_shift"]
        red_shift = params["red_shift"]

        # Split channels and apply shifts
        b, g, r = cv2.split(image)
        b = cv2.add(b, blue_shift)
        g = cv2.add(g, green_shift)
        r = cv2.add(r, red_shift)

        # Merge channels and return the result
        return cv2.merge([b, g, r])
