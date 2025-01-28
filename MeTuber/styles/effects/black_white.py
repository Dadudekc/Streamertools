import cv2
from ..base import Style

class BlackWhite(Style):
    """
    A style that converts an image to black and white based on a threshold.
    """
    name = "Black & White"
    category = "Effects"
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

    def define_parameters(self):
        """
        Define the parameters for the Black & White style.
        """
        return self.parameters

    def apply(self, image, params=None):
        """
        Apply the Black & White effect to an image.

        Args:
            image: Input image (NumPy array).
            params: Dictionary of parameters (e.g., threshold).

        Returns:
            Binary image (NumPy array).
        """
        if params is None:
            params = {}
        params = self.validate_params(params)

        # Retrieve the threshold value
        threshold = params.get("threshold", 128)

        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply binary thresholding
        _, bw = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        return bw
