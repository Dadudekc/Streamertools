import cv2
import numpy as np
from ..base import Style

class Glitch(Style):
    """
    Applies a glitch effect by randomly shifting color channels.
    """
    name = "Glitch"
    category = "Distortions"
    parameters = [
        {"name": "max_shift", "type": "int", "default": 10, "min": 0, "max": 50, "step": 1, "label": "Max Shift"},
        {"name": "num_shifts", "type": "int", "default": 5, "min": 1, "max": 20, "step": 1, "label": "Number of Shifts"},
    ]

    def apply(self, image, params=None):
        """
        Applies a glitch effect by shifting random regions of color channels.

        :param image: Input BGR image.
        :param params: Dictionary of parameters for glitch effect.
        :return: Glitched image.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")

        # Validate and sanitize parameters
        params = self.validate_params(params)

        # Extract parameters
        max_shift = params["max_shift"]
        num_shifts = params["num_shifts"]
        h, w = image.shape[:2]

        # Ensure image has at least 2 dimensions
        if len(image.shape) != 3 or image.shape[2] != 3:
            raise ValueError("Input image must be a BGR color image.")

        glitched_image = image.copy()

        # Apply random shifts to color channels
        for _ in range(num_shifts):
            channel = np.random.randint(0, 3)
            shift = np.random.randint(-max_shift, max_shift + 1)
            if shift > 0:
                glitched_image[:, :w - shift, channel] = image[:, shift:, channel]
                glitched_image[:, w - shift:, channel] = 0
            elif shift < 0:
                glitched_image[:, -shift:, channel] = image[:, :w + shift, channel]
                glitched_image[:, :-shift, channel] = 0

        return glitched_image
