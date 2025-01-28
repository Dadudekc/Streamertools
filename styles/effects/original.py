# styles/effects/original.py

from ..base import Style
import cv2
import numpy as np

class Original(Style):
    """
    Original style that returns the image without any modifications.
    """
    name = "Original"
    category = "Effects"
    parameters = []  # No parameters

    def apply(self, image, params=None):
        """
        Returns the original image without any modifications.

        Args:
            image (numpy.ndarray): The input image in BGR format.
            params (dict, optional): Not used.

        Returns:
            numpy.ndarray: The original image.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")
        return image.copy()

# Update effects/__init__.py to include Original
# Add the following lines:
# from .original import Original
# and include "Original" in __all__
