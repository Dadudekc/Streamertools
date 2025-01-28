# File: styles/basic/vibrant_color.py

import cv2
import numpy as np
from ..base import Style


class VibrantColor(Style):
    """
    Enhances the vibrancy of colors in the image by increasing saturation.
    """

    name = "Vibrant Color"
    category = "Basic"
    parameters = [
        {
            "name": "intensity",
            "type": "float",
            "default": 1.5,
            "min": 0.5,
            "max": 3.0,
            "step": 0.1,
            "label": "Intensity",
        }
    ]

    def define_parameters(self):
        """
        Returns the parameter definitions for color vibrancy.
        """
        return self.parameters

    def apply(self, image, params=None):
        """
        Enhances the vibrancy of colors in the image.

        Args:
            image (numpy.ndarray): The input image in BGR format.
            params (dict, optional): Parameters for color vibrancy.

        Returns:
            numpy.ndarray: The image with enhanced vibrant colors.

        Raises:
            ValueError: If the input image is None or invalid.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")

        # Initialize params to an empty dictionary if None
        params = params or {}

        # Validate and sanitize parameters
        params = self.validate_params(params)
        intensity = params["intensity"]

        # Convert to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)

        # Enhance the saturation channel
        hsv[:, :, 1] *= intensity
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)  # Clamp saturation to valid range

        # Convert back to BGR color space
        vibrant_image = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

        return vibrant_image
