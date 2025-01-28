# File: styles/basic/brightness_only.py

import cv2
import numpy as np
from ..base import Style


class BrightnessOnly(Style):
    """
    Adjusts the brightness of the image.
    """

    name = "Brightness Only"
    category = "Basic"
    parameters = [
        {
            "name": "brightness",
            "type": "int",
            "default": 0,
            "min": -100,
            "max": 100,
            "step": 1,
            "label": "Brightness",
        }
    ]

    def define_parameters(self):
        """
        Returns the parameter definitions for brightness adjustment.
        """
        return self.parameters

    def apply(self, image, params=None):
        """
        Adjusts the brightness of the image.

        Args:
            image (numpy.ndarray): The input image in BGR format.
            params (dict, optional): Parameters for brightness adjustment.

        Returns:
            numpy.ndarray: The brightness-adjusted image.

        Raises:
            ValueError: If the input image is None or invalid.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")

        # Initialize params to an empty dictionary if None
        params = params or {}

        # Validate and sanitize parameters
        params = self.validate_params(params)

        brightness = params["brightness"]

        # Convert to HSV for brightness adjustment
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        # Apply brightness adjustment with clamping
        v = np.clip(v.astype(int) + brightness, 0, 255).astype(np.uint8)

        # Merge adjusted channels and convert back to BGR
        adjusted = cv2.cvtColor(cv2.merge((h, s, v)), cv2.COLOR_HSV2BGR)

        return adjusted
