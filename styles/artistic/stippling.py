import cv2
import numpy as np
from styles.base import Style

class Stippling(Style):
    """
    A style that applies a stippled effect to the image.
    """
    name = "Stippling"
    category = "Artistic Styles"
    parameters = [
        {
            "name": "dot_density",
            "type": "int",
            "default": 10,
            "min": 1,
            "max": 50,
            "step": 1,
            "label": "Dot Density"
        },
        {
            "name": "contrast_adjustment",
            "type": "float",
            "default": 1.0,
            "min": 0.5,
            "max": 3.0,
            "step": 0.1,
            "label": "Contrast Adjustment"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        params = self.validate_params(params)

        dot_density = params["dot_density"]
        contrast = params["contrast_adjustment"]

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Increase contrast
        gray = cv2.convertScaleAbs(gray, alpha=contrast, beta=0)

        # Create stippled effect
        stippled = np.zeros_like(gray)
        for y in range(0, gray.shape[0], dot_density):
            for x in range(0, gray.shape[1], dot_density):
                if gray[y, x] > 128:  # Threshold for dot placement
                    stippled[y:y + dot_density, x:x + dot_density] = 255

        return stippled
