# MeTuber\styles\effects\vibrant_color.py

import cv2
import numpy as np
from styles.base import Style  # Adjust the import path as needed


class VibrantColor(Style):
    """
    Enhances the vibrancy of colors in the image by increasing saturation.
    """
    name = "Vibrant Color"
    category = "Basic"

    def define_parameters(self):
        """
        Define parameters for the VibrantColor style.

        :return: List of parameter dictionaries.
        """
        return [
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
            raise ValueError("Invalid image provided. Expected a NumPy array.")
        if not isinstance(image, np.ndarray):
            raise ValueError("Invalid image provided. Expected a NumPy array.")
        if image.dtype != np.uint8:
            raise ValueError("Input image must have dtype of np.uint8.")
        if image.ndim != 3 or image.shape[2] != 3:
            raise ValueError("Input image must be a 3-channel BGR image.")

        # Validate and sanitize parameters
        params = params or {}
        params = self.validate_params(params)
        intensity = params["intensity"]

        # Convert to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)

        # Enhance the saturation channel
        hsv[:, :, 1] = hsv[:, :, 1] * intensity
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)  # Clamp saturation to valid range

        # Convert back to BGR color space
        vibrant_image = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

        return vibrant_image
