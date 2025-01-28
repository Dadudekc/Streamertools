# File: styles/basic/brightness_only.py

import cv2
import numpy as np
from MeTuber.styles.base import Style

class BrightnessOnly(Style):
    """
    Adjusts the brightness of the video frame.
    """
    name = "Brightness Only"
    category = "Basic"

    def define_parameters(self):
        """
        Define parameters for brightness adjustment.

        Returns:
            list: List containing brightness parameter.
        """
        return [
            {
                "name": "brightness",
                "label": "Brightness",
                "type": "int",
                "min": -100,
                "max": 100,
                "step": 1,
                "default": 0
            }
        ]

    def apply(self, frame, params=None):
        """
        Adjust the brightness of the frame.

        Args:
            frame (numpy.ndarray): The input video frame.
            params (dict): Parameters for brightness adjustment.

        Returns:
            numpy.ndarray: The brightness-adjusted frame.
        """
        if frame is None:
            raise ValueError("Input image cannot be None.")
        if params is None:
            params = {}

        brightness = params.get("brightness", 0)

        # Validate brightness range
        if not -100 <= brightness <= 100:
            raise ValueError("Parameter 'brightness' must be between -100 and 100.")

        # Convert to HSV to adjust brightness
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        # Adjust brightness with clamping
        v = np.clip(v.astype(int) + brightness, 0, 255).astype(np.uint8)

        final_hsv = cv2.merge((h, s, v))
        frame_bright = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return frame_bright
