import cv2
from styles.base import Style
from typing import Optional, Dict, Any
import numpy as np

class BlurStyle(Style):
    """
    A style that applies a Gaussian blur to the image.
    """
    name = "Blur"
    category = "Effects"
    parameters = [
        {"name": "kernel_size", "type": "int", "default": 5, "min": 1, "max": 31, "step": 2, "label": "Kernel Size"}
    ]

    def apply(self, image: np.ndarray, params: Optional[Dict[str, Any]] = None) -> np.ndarray:
        params = self.validate_params(params)

        kernel_size = params["kernel_size"]

        # Ensure kernel size is odd
        if kernel_size % 2 == 0:
            kernel_size += 1

        blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        return blurred
