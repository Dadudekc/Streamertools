import cv2
from ..base import Style

class EdgeDetection(Style):
    """
    A style that applies edge detection using the Canny method.
    """
    name = "Edge Detection"
    parameters = [
        {
            "name": "threshold1",
            "type": "int",
            "default": 100,
            "min": 0,
            "max": 500,
            "step": 1,
            "label": "Threshold 1"
        },
        {
            "name": "threshold2",
            "type": "int",
            "default": 200,
            "min": 0,
            "max": 500,
            "step": 1,
            "label": "Threshold 2"
        }
    ]

    def apply(self, image, params=None):
        """
        Apply the edge detection style using the validated parameters.
        :param image: Input BGR image.
        :param params: Dictionary of parameters.
        :return: Processed image with edges highlighted.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")
        if len(image.shape) != 3 or image.shape[2] != 3:
            raise ValueError("Input image must be a BGR color image.")

        if params is None:
            params = {}
        params = self.validate_params(params)

        threshold1 = params["threshold1"]
        threshold2 = params["threshold2"]

        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Canny edge detection
        edges = cv2.Canny(gray, threshold1, threshold2)
        return edges
