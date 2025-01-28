import cv2
import numpy as np
from styles.base import Style


class GammaCorrection(Style):
    name = "Gamma Correction"
    parameters = [
        {
            "name": "gamma",
            "type": "float",
            "default": 1.0,
            "min": 0.1,
            "max": 3.0,
            "step": 0.1,
            "label": "Gamma"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        params = self.validate_params(params)

        gamma = params["gamma"]
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in range(256)]).astype("uint8")
        corrected = cv2.LUT(image, table)
        return corrected
