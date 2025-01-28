import cv2
import numpy as np
from styles.base import Style

class Sharpen(Style):
    name = "Sharpen"
    category = "Adjustments"
    parameters = [
        {"name": "kernel_size", "type": "int", "default": 3, "min": 1, "max": 5, "step": 2, "label": "Kernel Size"},
        {"name": "strength", "type": "float", "default": 1.0, "min": 0.5, "max": 3.0, "step": 0.1, "label": "Strength"}
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        params = self.validate_params(params)

        kernel_size = params["kernel_size"]
        strength = params["strength"]
        kernel = np.array([
            [0, -1, 0],
            [-1, 5 + strength, -1],
            [0, -1, 0]
        ])
        sharpened = cv2.filter2D(image, -1, kernel)
        return sharpened
