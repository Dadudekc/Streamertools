# File: styles/color_filters/invert_filter.py

import cv2
import numpy as np
from ..base import Style


class InvertFilter(Style):
    """
    Inverts the colors of the image, creating a negative effect.
    """

    name = "Invert Filter"
    category = "Color Filters"
    parameters = []  # No parameters required

    def define_parameters(self):
        """
        Returns the parameter definitions for this effect.
        """
        return self.parameters

    def apply(self, image, params=None):
        """
        Applies a color inversion effect to the image.

        Args:
            image (numpy.ndarray): The input image in BGR format.
            params (dict, optional): Parameters for the filter (not used).

        Returns:
            numpy.ndarray: The inverted image.

        Raises:
            ValueError: If the input image is None or invalid.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")

        if not isinstance(image, np.ndarray):
            raise ValueError("Invalid image provided. Expected a NumPy array.")

        return cv2.bitwise_not(image)
