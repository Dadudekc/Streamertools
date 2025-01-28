import cv2
import numpy as np
from ..base import Style


class HoughLines(Style):
    """
    Detects and draws lines on the image using the Probabilistic Hough Line Transform.
    """

    name = "Hough Lines"
    category = "Effects"
    parameters = [
        {
            "name": "threshold",
            "type": "int",
            "default": 150,
            "min": 0,
            "max": 300,
            "step": 10,
            "label": "Threshold",
        },
        {
            "name": "minLineLength",
            "type": "int",
            "default": 100,
            "min": 50,
            "max": 300,
            "step": 10,
            "label": "Min Line Length",
        },
        {
            "name": "maxLineGap",
            "type": "int",
            "default": 10,
            "min": 0,
            "max": 100,
            "step": 5,
            "label": "Max Line Gap",
        },
    ]

    def apply(self, image, params=None):
        """
        Detects lines in the image using the Probabilistic Hough Line Transform
        and draws them on the image.

        Args:
            image (numpy.ndarray): The input image in BGR format.
            params (dict, optional): Parameters for Hough Lines detection.

        Returns:
            numpy.ndarray: The image with detected lines drawn.

        Raises:
            ValueError: If the input image is None or invalid.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")
        if params is None:
            params = {}

        params = self.validate_params(params)

        threshold = params["threshold"]
        minLineLength = params["minLineLength"]
        maxLineGap = params["maxLineGap"]

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Canny edge detection
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        # Detect lines using the Probabilistic Hough Line Transform
        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi / 180,
            threshold=threshold,
            minLineLength=minLineLength,
            maxLineGap=maxLineGap,
        )

        # Draw the detected lines on the original image
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        return image
    
class CannyEdge(Style):
    name = "Canny Edge"
    category = "Effects"
    parameters = [
        {"name": "threshold1", "type": "int", "default": 100, "min": 0, "max": 300, "step": 10, "label": "Threshold 1"},
        {"name": "threshold2", "type": "int", "default": 200, "min": 0, "max": 300, "step": 10, "label": "Threshold 2"},
        {"name": "apertureSize", "type": "int", "default": 3, "min": 3, "max": 7, "step": 2, "label": "Aperture Size"},
    ]

    def apply(self, image, params=None):
        if image is None:
            raise ValueError("Input image cannot be None.")
        if params is None:
            params = {}

        # Custom validation for apertureSize
        apertureSize = params.get("apertureSize", self.default_params["apertureSize"])
        if apertureSize % 2 == 0 or not (3 <= apertureSize <= 7):
            raise ValueError("Aperture size must be an odd number between 3 and 7.")

        params = self.validate_params(params)
        threshold1 = params["threshold1"]
        threshold2 = params["threshold2"]

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, threshold1, threshold2, apertureSize=apertureSize, L2gradient=True)

        return edges