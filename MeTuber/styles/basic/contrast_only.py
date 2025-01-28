# File: styles/basic/contrast_only.py

import cv2
from ..base import Style


class ContrastOnly(Style):
    """
    Adjusts the contrast of the image.
    """

    name = "Contrast Only"
    category = "Basic"
    parameters = [
        {
            "name": "contrast",
            "type": "float",
            "default": 1.0,
            "min": 0.5,
            "max": 3.0,
            "step": 0.1,
            "label": "Contrast",
        }
    ]

    def define_parameters(self):
        """
        Returns the parameter definitions for contrast adjustment.
        """
        return self.parameters

    def apply(self, image, params=None):
        """
        Adjusts the contrast of the image by scaling the alpha value.

        Args:
            image (numpy.ndarray): The input image in BGR format.
            params (dict, optional): Parameters for contrast adjustment.

        Returns:
            numpy.ndarray: The contrast-adjusted image.

        Raises:
            ValueError: If the input image is None or invalid.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")

        # Initialize params to an empty dictionary if None
        params = params or {}

        # Validate and sanitize parameters
        params = self.validate_params(params)

        contrast = params["contrast"]

        # Apply contrast adjustment
        # alpha is the contrast factor
        # beta=0 means no change in brightness
        adjusted = cv2.convertScaleAbs(image, alpha=contrast, beta=0)

        return adjusted
