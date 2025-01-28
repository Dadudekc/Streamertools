import numpy as np
from styles.base import Style


class Solarize(Style):
    """
    A style that applies a solarize effect to the input image.
    """
    name = "Solarize"
    category = "Adjustments"

    def define_parameters(self):
        """
        Define parameters for the Solarize style.

        Returns:
            list: List of parameter dictionaries for the Solarize effect.
        """
        return [
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

    def apply(self, image, params=None):
        """
        Apply the solarize effect to the input image.

        Args:
            image (np.ndarray): Input image as a NumPy array.
            params (dict, optional): Dictionary of parameters.

        Returns:
            np.ndarray: Solarized image.

        Raises:
            ValueError: If the input image is None or invalid.
        """
        # Validate the input image
        if image is None:
            raise ValueError("Input image cannot be None.")
        if not isinstance(image, np.ndarray):
            raise ValueError("Input must be a valid NumPy array.")
        if image.dtype != np.uint8:
            raise ValueError("Input image must have dtype of np.uint8.")

        # Validate and retrieve parameters
        params = self.validate_params(params or {})
        threshold = params["threshold"]

        # Apply the solarize effect
        solarized = np.where(image < threshold, image, 255 - image)

        return solarized.astype(np.uint8)
