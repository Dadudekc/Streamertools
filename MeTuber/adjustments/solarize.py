import numpy as np
from styles.base import Style


class Solarize(Style):
    """
    A style that solarizes the input image.
    """
    name = "Solarize"

    def define_parameters(self):
        """
        Define parameters for the Solarize style.
        
        :return: List of parameter dictionaries.
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

        :param image: Input image as a NumPy array.
        :param params: Dictionary of parameters.
        :return: Solarized image.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")
        if not isinstance(image, np.ndarray):
            raise ValueError("Input must be a valid NumPy array.")
        if image.dtype != np.uint8:
            raise ValueError("Input image must have dtype of np.uint8.")

        # Validate parameters
        params = params or {}
        params = self.validate_params(params)
        threshold = params["threshold"]

        # Solarize the image
        solarized = np.where(image < threshold, image, 255 - image)
        return solarized.astype(np.uint8)
