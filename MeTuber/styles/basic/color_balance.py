# File: styles/basic/color_balance.py

import cv2
import numpy as np
from MeTuber.styles.base import Style

class ColorBalance(Style):
    """
    Adjusts the color balance of an image by modifying the blue, green, and red channels.
    """
    name = "Color Balance"
    category = "Basic"

    def define_parameters(self):
        """
        Define parameters for color balance adjustment.

        Returns:
            list: List containing parameters for blue, green, and red shifts.
        """
        return [
            {
                "name": "blue_shift",
                "label": "Blue Shift",
                "type": "int",
                "min": -50,
                "max": 50,
                "step": 1,
                "default": 0
            },
            {
                "name": "green_shift",
                "label": "Green Shift",
                "type": "int",
                "min": -50,
                "max": 50,
                "step": 1,
                "default": 0
            },
            {
                "name": "red_shift",
                "label": "Red Shift",
                "type": "int",
                "min": -50,
                "max": 50,
                "step": 1,
                "default": 0
            }
        ]

    def apply(self, frame, params=None):
        """
        Adjust the color balance of the frame.

        Args:
            frame (numpy.ndarray): Input image.
            params (dict): Dictionary containing parameters for color balance adjustment.

        Returns:
            numpy.ndarray: Color-balanced image.
        """
        if frame is None:
            raise ValueError("Input image cannot be None.")
        if params is None:
            params = {}

        # Validate and retrieve parameters
        params = self.validate_params(params)
        blue_shift = params.get("blue_shift", 0)
        green_shift = params.get("green_shift", 0)
        red_shift = params.get("red_shift", 0)

        # Split the channels
        blue, green, red = cv2.split(frame)

        # Adjust each channel
        blue = np.clip(blue.astype(int) + blue_shift, 0, 255).astype(np.uint8)
        green = np.clip(green.astype(int) + green_shift, 0, 255).astype(np.uint8)
        red = np.clip(red.astype(int) + red_shift, 0, 255).astype(np.uint8)

        # Merge channels back
        balanced_frame = cv2.merge((blue, green, red))
        return balanced_frame
