# styles\basic\brightness_only.py

import cv2
from ..base import Style


class BrightnessOnly(Style):
    """
    Adjusts the brightness of the image.
    """

    name = "Brightness Only"
    category = "Basic"
    parameters = [
        {
            "name": "brightness",
            "type": "int",
            "default": 0,
            "min": -100,
            "max": 100,
            "step": 5,
            "label": "Brightness",
        }
    ]

    def apply(self, image, params=None):
        """
        Adjusts the brightness of the image by adding a beta value.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")

        # Initialize params if None
        params = params or {}

        # Validate and sanitize parameters
        params = self.validate_params(params)

        brightness = params["brightness"]

        # Apply brightness adjustment
        adjusted = cv2.convertScaleAbs(image, alpha=1.0, beta=brightness)

        return adjusted
