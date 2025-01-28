# styles/effects/misc/emboss_contrast.py

import cv2
import numpy as np
from ..base import Style


class EmbossContrast(Style):
    """
    Applies an emboss effect and adjusts the contrast of the image.
    """

    name = "Emboss & Contrast"
    category = "Effects"
    parameters = [
        {
            "name": "kernel_size",
            "type": "int",
            "default": 3,
            "min": 1,
            "max": 5,
            "step": 2,
            "label": "Kernel Size",
        },
        {
            "name": "scale",
            "type": "float",
            "default": 1.0,
            "min": 0.5,
            "max": 3.0,
            "step": 0.1,
            "label": "Scale",
        },
        {
            "name": "contrast",
            "type": "float",
            "default": 1.0,
            "min": 0.5,
            "max": 3.0,
            "step": 0.1,
            "label": "Contrast",
        },
    ]

    def apply(self, image, params=None):
        """
        Applies an emboss effect and adjusts the contrast of the image.

        Args:
            image (numpy.ndarray): The input image in BGR format.
            params (dict, optional): Parameters for emboss and contrast adjustment.

        Returns:
            numpy.ndarray: The embossed and contrast-adjusted image.

        Raises:
            ValueError: If the input image is None or invalid.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")

        # Validate and sanitize parameters
        params = self.validate_params(params)

        kernel_size = params["kernel_size"]
        scale = params["scale"]
        contrast = params["contrast"]

        # Define the emboss kernel
        emboss_kernel = np.array(
            [[-2, -1, 0],
             [-1, 1, 1],
             [0, 1, 2]],
            dtype=np.float32,
        )

        # Apply the emboss filter
        embossed = cv2.filter2D(image, -1, emboss_kernel)

        # Scale the embossed image
        embossed = cv2.convertScaleAbs(embossed, alpha=scale, beta=128)

        # Adjust contrast
        contrasted = cv2.convertScaleAbs(embossed, alpha=contrast, beta=0)

        return contrasted
