# File: styles/basic/color_balance.py

import cv2
import numpy as np
from ..base import Style


class ColorBalance(Style):
    """
    Adjusts the color balance of an image by modifying the blue, green, and red channels.
    """

    name = "Color Balance"
    category = "Basic"
    parameters = [
        {
            "name": "blue_shift",
            "type": "int",
            "default": 0,
            "min": -50,
            "max": 50,
            "step": 1,
            "label": "Blue Shift",
        },
        {
            "name": "green_shift",
            "type": "int",
            "default": 0,
            "min": -50,
            "max": 50,
            "step": 1,
            "label": "Green Shift",
        },
        {
            "name": "red_shift",
            "type": "int",
            "default": 0,
            "min": -50,
            "max": 50,
            "step": 1,
            "label": "Red Shift",
        },
    ]

    def define_parameters(self):
        """
        Returns the parameter definitions for color balance adjustment.
        """
        return self.parameters

    def apply(self, image, params=None):
        """
        Adjusts the color balance of the image.

        Args:
            image (numpy.ndarray): The input image in BGR format.
            params (dict, optional): Parameters for color balance adjustment.

        Returns:
            numpy.ndarray: The color-balanced image.

        Raises:
            ValueError: If the input image is None or invalid.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")

        # Initialize params to an empty dictionary if None
        params = params or {}

        # Validate and sanitize parameters
        params = self.validate_params(params)

        blue_shift = params["blue_shift"]
        green_shift = params["green_shift"]
        red_shift = params["red_shift"]

        # Split the channels
        blue, green, red = cv2.split(image)

        # Adjust each channel with clipping
        blue = np.clip(blue.astype(int) + blue_shift, 0, 255).astype(np.uint8)
        green = np.clip(green.astype(int) + green_shift, 0, 255).astype(np.uint8)
        red = np.clip(red.astype(int) + red_shift, 0, 255).astype(np.uint8)

        # Merge channels back
        adjusted = cv2.merge((blue, green, red))

        return adjusted
