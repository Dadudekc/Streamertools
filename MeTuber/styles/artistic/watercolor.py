import cv2
import numpy as np
from styles.base import Style  # Absolute import


class Watercolor(Style):
    """
    Applies a watercolor effect to the image.
    """
    name = "Watercolor"
    category = "Artistic"

    def define_parameters(self):
        """
        Define parameters for the Watercolor style.
        
        :return: List of parameter dictionaries.
        """
        return [
            {
                "name": "sigma_s",
                "type": "int",
                "default": 60,
                "min": 10,
                "max": 100,
                "step": 10,
                "label": "Sigma S",
            },
            {
                "name": "sigma_r",
                "type": "float",
                "default": 0.5,
                "min": 0.1,
                "max": 1.0,
                "step": 0.1,
                "label": "Sigma R",
            },
        ]

    def apply(self, image, params=None):
        """
        Applies a watercolor effect to the image using OpenCV's stylization.

        Args:
            image (numpy.ndarray): The input image in BGR format.
            params (dict, optional): Parameters for watercolor effect.

        Returns:
            numpy.ndarray: The watercolor-stylized image.

        Raises:
            ValueError: If the input image is None or invalid.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")
        if not isinstance(image, np.ndarray):
            raise ValueError("Input must be a valid NumPy array.")
        if image.ndim != 3 or image.shape[2] != 3:
            raise ValueError("Input image must be a 3-channel BGR image.")

        # Validate and sanitize parameters
        params = params or {}
        params = self.validate_params(params)

        sigma_s = params["sigma_s"]
        sigma_r = params["sigma_r"]

        # Apply stylization using OpenCV's stylization function
        watercolor = cv2.stylization(image, sigma_s=sigma_s, sigma_r=sigma_r)

        return watercolor
