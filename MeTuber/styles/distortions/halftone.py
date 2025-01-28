import cv2
import numpy as np
from ..base import Style


class Halftone(Style):
    """
    Applies a halftone effect to the image with adjustable dot size and threshold.
    """

    name = "Halftone"
    category = "Distortions"

    def define_parameters(self):
        """
        Defines the parameters for the Halftone effect.
        """
        return [
            {
                "name": "dot_size",
                "type": "int",
                "default": 5,
                "min": 1,
                "max": 20,
                "step": 1,
                "label": "Dot Size",
            },
            {
                "name": "threshold",
                "type": "int",
                "default": 127,
                "min": 0,
                "max": 255,
                "step": 5,
                "label": "Threshold",
            },
        ]

    def apply(self, image, params=None):
        """
        Applies a halftone effect by thresholding and adding dot patterns.

        Args:
            image (numpy.ndarray): The input image in BGR format.
            params (dict, optional): Parameters for halftone effect.

        Returns:
            numpy.ndarray: The image with a halftone effect.

        Raises:
            ValueError: If the input image is None or invalid.
        """
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Invalid image provided. Expected a NumPy array.")

        # Validate and sanitize parameters
        params = self.validate_params(params or {})

        dot_size = params["dot_size"]
        threshold = params["threshold"]

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Handle special cases for threshold
        if threshold == 0:
            return np.full_like(image, 0)  # Completely black image
        elif threshold == 255:
            return np.full_like(image, 255)  # Completely white image

        # Apply binary thresholding
        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

        # Create an empty canvas for the halftone effect
        halftone = np.full_like(image, 255)  # White background

        # Draw dots for black pixels in the binary image
        for y in range(0, binary.shape[0], dot_size * 2):
            for x in range(0, binary.shape[1], dot_size * 2):
                if binary[y, x] == 0:  # Black pixel in binary image
                    cv2.circle(halftone, (x, y), dot_size, (0, 0, 0), -1)

        return halftone
