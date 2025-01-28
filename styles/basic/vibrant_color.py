# styles/effects/vibrant_color.py

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
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Invalid image provided. Expected a NumPy array.")

        # Use default parameters if none are provided
        if params is None:
            params = self.default_params

        # Validate and sanitize parameters
        params = self.validate_params(params)
        intensity = params["intensity"]

        # Convert to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)

        # Enhance the saturation channel
        hsv[:, :, 1] = hsv[:, :, 1] * intensity
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)  # Clamp saturation to valid range

        # Convert back to BGR color space
        vibrant_image = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

        # Check if the image is modified
        if np.array_equal(image, vibrant_image):
            raise RuntimeError("Image was not modified. Check the vibrancy logic.")

        return vibrant_image
