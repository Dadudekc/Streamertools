import cv2
from styles.base import Style

class Threshold(Style):
    name = "Threshold"
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

        if len(image.shape) == 3:  # If color image, convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # Use cv2.threshold with THRESH_BINARY to handle pixels >= threshold
        _, thresh = cv2.threshold(gray, threshold - 1, 255, cv2.THRESH_BINARY)
        return thresh
