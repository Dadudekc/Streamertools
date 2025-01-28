import cv2
import numpy as np
from styles.base import Style

class Vibrance(Style):
    name = "Vibrance"
    category = "Adjustments"
    parameters = [
        {
            "name": "vibrance",
            "type": "float",
            "default": 1.0,
            "min": 0.0,
            "max": 3.0,
            "step": 0.1,
            "label": "Vibrance"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        params = self.validate_params(params)

        vibrance = params["vibrance"]
        # Convert grayscale to BGR to ensure 3 channels
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] *= vibrance
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
        hsv = hsv.astype(np.uint8)
        vibrant = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return vibrant
