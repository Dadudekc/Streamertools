import cv2
import numpy as np
from styles.base import Style

class Emboss(Style):
    name = "Emboss"
    parameters = [
        {"name": "kernel_size", "type": "int", "default": 3, "min": 1, "max": 5, "step": 2, "label": "Kernel Size"},
        {"name": "scale", "type": "float", "default": 1.0, "min": 0.1, "max": 3.0, "step": 0.1, "label": "Scale"}
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        params = self.validate_params(params)

        kernel_size = params["kernel_size"]
        scale = params["scale"]
        kernel = np.array([
            [-2, -1, 0],
            [-1,  1, 1],
            [0,   1, 2]
        ])
        embossed = cv2.filter2D(image, -1, kernel) * scale + 128
        embossed = np.clip(embossed, 0, 255).astype(np.uint8)
        return embossed
