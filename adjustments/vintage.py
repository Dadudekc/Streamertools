import cv2
import numpy as np
from styles.base import Style


class Vintage(Style):
    name = "Vintage"
    parameters = [
        {
            "name": "vintage_strength",
            "type": "float",
            "default": 0.5,
            "min": 0.0,
            "max": 1.0,
            "step": 0.1,
            "label": "Vintage Strength"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        params = self.validate_params(params)

        strength = params["vintage_strength"]
        sepia_filter = np.array([[0.272, 0.534, 0.131],
                                 [0.349, 0.686, 0.168],
                                 [0.393, 0.769, 0.189]])
        sepia = cv2.transform(image, sepia_filter)
        sepia = np.clip(sepia, 0, 255).astype(np.uint8)

        vintage = cv2.addWeighted(image, 1 - strength, sepia, strength, 0)
        return vintage
