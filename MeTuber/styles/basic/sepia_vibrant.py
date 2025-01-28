# File: styles/basic/sepia_vibrant.py

import cv2
import numpy as np
from ..base import Style


class SepiaVibrant(Style):
    """
    Applies a sepia filter and enhances the vibrancy of colors in the image.
    """

    name = "Sepia Vibrant"
    category = "Basic"
    parameters = [
        {
            "name": "sepia_intensity",
            "type": "float",
            "default": 1.0,
            "min": 0.0,
            "max": 2.0,
            "step": 0.1,
            "label": "Sepia Intensity",
        },
        {
            "name": "vibrance",
            "type": "float",
            "default": 1.0,
            "min": 0.0,
            "max": 3.0,
            "step": 0.1,
            "label": "Vibrance",
        },
    ]

    def __init__(self):
        # Initialize default_params from parameters
        self.default_params = {param["name"]: param["default"] for param in self.parameters}

    def define_parameters(self):
        """
        Returns the parameters for the Sepia Vibrant style.
        """
        return self.parameters

    def apply(self, image, params=None):
        """
        Applies a sepia filter and enhances the vibrancy of colors in the image.

        Args:
            image (numpy.ndarray): The input image in BGR format.
            params (dict, optional): Parameters for sepia and vibrancy.

        Returns:
            numpy.ndarray: The image with sepia and vibrant color effects.

        Raises:
            ValueError: If the input image is None or invalid.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")

        # Initialize params with default parameters if None
        if params is None:
            params = self.default_params

        # Validate and sanitize parameters
        params = self.validate_params(params)

        sepia_intensity = params["sepia_intensity"]
        vibrance = params["vibrance"]

        # Define the sepia filter
        sepia_filter = np.array(
            [[0.272, 0.534, 0.131],
             [0.349, 0.686, 0.168],
             [0.393, 0.769, 0.189]],
            dtype=np.float32,
        )

        # Apply sepia filter
        sepia = cv2.transform(image, sepia_filter)

        # Scale sepia intensity
        sepia = np.clip(sepia * sepia_intensity, 0, 255).astype(np.uint8)

        # Convert to HSV to adjust vibrance
        hsv = cv2.cvtColor(sepia, cv2.COLOR_BGR2HSV).astype(np.float32)

        # Enhance saturation (Vibrance)
        hsv[:, :, 1] *= vibrance
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)

        # Convert back to BGR
        vibrant = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

        return vibrant
