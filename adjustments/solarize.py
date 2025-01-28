import numpy as np
from styles.base import Style

class Solarize(Style):
    name = "Solarize"
    parameters = [
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
        if params is None:
            params = {}
        params = self.validate_params(params)

        threshold = params["threshold"]
        # Ensure image is a NumPy array
        solarized = np.where(image < threshold, image, 255 - image)
        return solarized.astype(np.uint8)
