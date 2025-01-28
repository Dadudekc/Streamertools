import cv2
from styles.base import Style

class BrightnessContrast(Style):
    name = "Brightness & Contrast"
    category = "Adjustments"
    parameters = [
        {"name": "brightness", "type": "int", "default": 0, "min": -100, "max": 100, "step": 5, "label": "Brightness"},
        {"name": "contrast", "type": "float", "default": 1.0, "min": 0.5, "max": 3.0, "step": 0.1, "label": "Contrast"}
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        params = self.validate_params(params)

        brightness = params["brightness"]
        contrast = params["contrast"]
        adjusted = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
        return adjusted
