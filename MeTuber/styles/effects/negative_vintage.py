import cv2
import numpy as np
from ..base import Style

class NegativeVintage(Style):
    """
    Applies a negative vintage effect to the image with adjustable sepia intensity.
    """

    name = "Negative Vintage"
    category = "Effects"
    parameters = [
        {
            "name": "sepia_intensity",
            "type": "float",
            "default": 1.0,
            "min": 0.0,
            "max": 2.0,
            "step": 0.1,
            "label": "Sepia Intensity",
        }
    ]

    def define_parameters(self):
        """
        Define the parameters for the Negative Vintage effect.
        """
        return self.parameters

    def apply(self, image, params=None):
        """
        Applies a negative vintage effect by inverting colors and applying a sepia filter.

        Args:
            image (numpy.ndarray): The input image in BGR format.
            params (dict, optional): Parameters for sepia intensity.

        Returns:
            numpy.ndarray: The image with a negative vintage effect.

        Raises:
            ValueError: If the input image is None or invalid.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")

        # Validate and sanitize parameters
        params = self.validate_params(params)

        sepia_intensity = params["sepia_intensity"]

        # Step 1: Invert the image
        inverted_image = cv2.bitwise_not(image)

        # Step 2: Apply sepia filter
        sepia_filter = np.array(
            [[0.272, 0.534, 0.131],
             [0.349, 0.686, 0.168],
             [0.393, 0.769, 0.189]],
            dtype=np.float32,
        )

        # Transform the inverted image using the sepia filter
        sepia = cv2.transform(inverted_image, sepia_filter)

        # Scale the sepia effect by the sepia intensity parameter
        sepia = np.clip(sepia * sepia_intensity, 0, 255).astype(np.uint8)

        return sepia
