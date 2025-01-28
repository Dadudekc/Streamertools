import cv2
import numpy as np
from styles.base import Style


class Threshold(Style):
    """
    Applies a binary threshold to the input image.
    """
    name = "Threshold"
    category = "Adjustments"

    def define_parameters(self):
        """
        Define parameters for the Threshold style.

        :return: List of parameter dictionaries.
        """
        return [
            {
                "name": "threshold",
                "type": "int",
                "default": 128,
                "min": 0,
                "max": 255,
                "step": 1,
                "label": "Threshold"
            }
        ]

    def apply(self, image, params=None):
        """
        Apply a binary threshold to the input image.

        :param image: Input image (grayscale or BGR) as a NumPy array.
        :param params: Dictionary of parameters.
        :return: Thresholded image.
        :raises ValueError: If the input image is invalid.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")
        if not isinstance(image, np.ndarray):
            raise ValueError("Input image must be a NumPy array.")
        if image.dtype != np.uint8:
            raise ValueError("Input image must have dtype np.uint8.")

        # Validate and sanitize parameters
        params = params or {}
        params = self.validate_params(params)

        threshold = params["threshold"]

        # Convert color image to grayscale
        if len(image.shape) == 3 and image.shape[2] == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # Apply thresholding
        _, thresh = cv2.threshold(gray, threshold - 1, 255, cv2.THRESH_BINARY)
        return thresh
