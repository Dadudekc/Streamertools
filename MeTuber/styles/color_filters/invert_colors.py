# File: styles/color_filters/invert_colors.py

import cv2
from ..base import Style

class InvertColors(Style):
    """
    Inverts the colors of an image.
    """
    name = "Invert Colors"
    category = "Color Filters"
    parameters = []  # No parameters for this effect

    def define_parameters(self):
        """
        Defines parameters for the Invert Colors effect.
        """
        return self.parameters

    def apply(self, frame, params=None):
        """
        Apply the invert colors effect.

        Args:
            frame (numpy.ndarray): The input image.
            params (dict, optional): Parameters for the effect (not used).

        Returns:
            numpy.ndarray: The color-inverted image.

        Raises:
            ValueError: If the input image is None.
        """
        if frame is None:
            raise ValueError("Input image cannot be None.")
        return cv2.bitwise_not(frame)
