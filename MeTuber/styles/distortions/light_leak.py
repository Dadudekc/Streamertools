import cv2
import numpy as np
from ..base import Style

class LightLeak(Style):
    """
    Adds a customizable light leak effect to the image with adjustable intensity and color.
    """

    name = "Light Leak"
    category = "Distortions"

    def define_parameters(self):
        """
        Define the parameters for the Light Leak effect.
        """
        return [
            {
                "name": "leak_intensity",
                "type": "int",
                "default": 50,
                "min": 0,
                "max": 100,
                "step": 5,
                "label": "Leak Intensity",
            },
            {
                "name": "leak_color",
                "type": "str",
                "default": "Red",
                "label": "Leak Color",
                "options": ["Red", "Green", "Blue", "Yellow", "Cyan", "Magenta"],
            },
            {
                "name": "leak_position",
                "type": "str",
                "default": "Top Right",
                "label": "Leak Position",
                "options": ["Top Left", "Top Right", "Bottom Left", "Bottom Right"],
            },
        ]

    def apply(self, image, params=None):
        """
        Applies a light leak effect to the image.

        Args:
            image (numpy.ndarray): The input image in BGR format.
            params (dict, optional): Parameters for the light leak effect.

        Returns:
            numpy.ndarray: The image with the light leak effect applied.

        Raises:
            ValueError: If the input image is None or invalid.
        """
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Input image cannot be None and must be a NumPy array.")

        # Validate and sanitize parameters
        params = self.validate_params(params)
        intensity = params["leak_intensity"]
        color = params["leak_color"].lower()
        position = params["leak_position"].lower()

        # Define color mappings
        color_dict = {
            "red": (0, 0, 255),
            "green": (0, 255, 0),
            "blue": (255, 0, 0),
            "yellow": (0, 255, 255),
            "cyan": (255, 255, 0),
            "magenta": (255, 0, 255),
        }
        leak_color = color_dict.get(color, (0, 0, 255))

        # Determine light leak position
        h, w = image.shape[:2]
        radius = int(min(h, w) * 0.3)  # Radius proportional to the image dimensions
        position_dict = {
            "top left": (radius, radius),
            "top right": (w - radius, radius),
            "bottom left": (radius, h - radius),
            "bottom right": (w - radius, h - radius),
        }
        center = position_dict.get(position, (w - radius, radius))

        # Create an overlay for the light leak effect
        overlay = image.copy()
        cv2.circle(overlay, center, radius, leak_color, -1)

        # Blend the overlay with the original image
        output = cv2.addWeighted(image, 1 - intensity / 100, overlay, intensity / 100, 0)

        return output
