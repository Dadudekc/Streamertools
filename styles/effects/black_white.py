import cv2
from ..base import Style

class BlackWhite(Style):
    """
    A style that converts an image to black and white based on a threshold.
    """
    name = "Black & White"
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

        # Retrieve the threshold value
        threshold = params.get("threshold", 128)

        # Check if the threshold is within valid bounds
        if threshold < 0 or threshold > 255:
            raise ValueError("Threshold must be between 0 and 255.")

        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply binary thresholding
        _, bw = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        return bw
