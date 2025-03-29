# styles/effects/original.py

import cv2
from styles.base import Style

class Original(Style):
    """
    The Original style applies no changes to the frame.
    """
    name = "Original"
    category = "Effects"

    def define_parameters(self):
        """
        The Original style has no parameters.

        Returns:
            list: Empty list since there are no parameters.
        """
        return []

    def apply(self, frame, params):
        """
        Returns the frame as-is.

        Args:
            frame (numpy.ndarray): The input video frame.
            params (dict): Parameters for the style (unused).

        Returns:
            numpy.ndarray: The original video frame.
        """
        return frame
