import cv2
import numpy as np
from styles.base import Style
from typing import Optional, Dict, Any


class BlurStyle(Style):
    """
    A style that applies a Gaussian blur to the image.
    """

    name = "Blur"
    category = "Adjustments"  # Unified category as "Effects" for consistency
    parameters = [
        {
            "name": "kernel_size",
            "type": "int",
            "default": 5,
            "min": 1,
            "max": 31,
            "step": 2,
            "label": "Kernel Size",
        }
    ]

    def define_parameters(self):
        """
        Returns the list of parameters for the BlurStyle.
        """
        return self.parameters

    def apply(self, image: np.ndarray, params: Optional[Dict[str, Any]] = None) -> np.ndarray:
        """
        Applies a Gaussian blur to the image.

        Args:
            image (np.ndarray): The input image to be blurred.
            params (dict, optional): Parameters for the Gaussian blur.

        Returns:
            np.ndarray: The blurred image.

        Raises:
            ValueError: If the input image is None or invalid.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")

        # Validate and retrieve parameters
        params = self.validate_params(params)

        kernel_size = params["kernel_size"]

        # Ensure kernel size is odd (required for GaussianBlur)
        if kernel_size % 2 == 0:
            kernel_size += 1

        blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        return blurred
