import cv2
import numpy as np
from styles.base import Style


class HueSaturation(Style):
    name = "Hue & Saturation"
    parameters = [
        {
            "name": "hue",
            "type": "int",
            "default": 0,
            "min": -50,
            "max": 50,
            "step": 1,
            "label": "Hue"
        },
        {
            "name": "saturation",
            "type": "int",
            "default": 0,
            "min": -50,
            "max": 50,
            "step": 1,
            "label": "Saturation"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        params = self.validate_params(params)

        hue = params["hue"]
        saturation = params["saturation"]
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.int32)
        hsv[:, :, 0] = (hsv[:, :, 0] + hue) % 180
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] + saturation, 0, 255)
        hsv = hsv.astype(np.uint8)
        adjusted = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return adjusted
