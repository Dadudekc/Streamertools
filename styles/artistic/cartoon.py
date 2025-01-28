import cv2
from styles.base import Style
import numpy as np

class Cartoon(Style):
    """
    A style that applies a cartoon effect to the image.
    """
    name = "Cartoon"
    parameters = [
        {
            "name": "bilateral_filter_diameter",
            "type": "int",
            "default": 9,
            "min": 1,
            "max": 20,
            "step": 1,
            "label": "Bilateral Filter Diameter"
        },
        {
            "name": "bilateral_filter_sigmaColor",
            "type": "int",
            "default": 75,
            "min": 1,
            "max": 150,
            "step": 1,
            "label": "Bilateral Filter SigmaColor"
        },
        {
            "name": "bilateral_filter_sigmaSpace",
            "type": "int",
            "default": 75,
            "min": 1,
            "max": 150,
            "step": 1,
            "label": "Bilateral Filter SigmaSpace"
        },
        {
            "name": "canny_threshold1",
            "type": "int",
            "default": 100,
            "min": 0,
            "max": 500,
            "step": 1,
            "label": "Canny Threshold 1"
        },
        {
            "name": "canny_threshold2",
            "type": "int",
            "default": 200,
            "min": 0,
            "max": 500,
            "step": 1,
            "label": "Canny Threshold 2"
        }
    ]

    def apply(self, image, params=None):
        """
        Apply the cartoon effect using the validated parameters.
        :param image: Input BGR image.
        :param params: Dictionary of parameters.
        :return: Processed image with a cartoon effect.
        """
        if image is None or not isinstance(image, (np.ndarray,)):
            raise ValueError("Input image must be a valid NumPy array.")

        if params is None:
            params = {}

        # Validate parameters
        params = self.validate_params(params)

        # Extract validated parameters
        d = params["bilateral_filter_diameter"]
        sigmaColor = params["bilateral_filter_sigmaColor"]
        sigmaSpace = params["bilateral_filter_sigmaSpace"]
        threshold1 = params["canny_threshold1"]
        threshold2 = params["canny_threshold2"]

        # Apply bilateral filter to smoothen the image
        filtered = cv2.bilateralFilter(image, d, sigmaColor, sigmaSpace)

        # Detect edges using Canny
        gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, threshold1, threshold2)

        # Convert edges to BGR for bitwise_and operation
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # Combine the edges and the filtered image
        cartoonized = cv2.bitwise_and(filtered, edges_colored)
        return cartoonized
