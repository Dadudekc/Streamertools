# styles/effects/oil_painting.py

import cv2
from ..base import Style


class OilPainting(Style):
    """
    Applies an oil painting effect to the image.
    """

    name = "Oil Painting"
    category = "Artistic"
    parameters = [
        {
            "name": "size",
            "type": "int",
            "default": 7,
            "min": 1,
            "max": 15,
            "step": 2,
            "label": "Size",
        },
        {
            "name": "dyn_ratio",
            "type": "float",
            "default": 1.0,
            "min": 0.0,
            "max": 2.0,
            "step": 0.1,
            "label": "Dyn Ratio",
        },
    ]

    def apply(self, image, params=None):
        """
        Applies an oil painting effect to the image using OpenCV's stylization.

        Args:
            image (numpy.ndarray): The input image in BGR format.
            params (dict, optional): Parameters for oil painting effect.

        Returns:
            numpy.ndarray: The oil painting-stylized image.

        Raises:
            ValueError: If the input image is None or invalid.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")

        # Validate and sanitize parameters
        params = self.validate_params(params)

        size = params["size"]
        dyn_ratio = params["dyn_ratio"]

        # Apply oil painting effect
        oil_painting = cv2.xphoto.oilPainting(image, size=size, dynRatio=dyn_ratio)

        return oil_painting
