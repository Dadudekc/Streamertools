# styles/effects/blur_motion.py

import cv2
import numpy as np
from ..base import Style
from typing import Optional, Dict, Any

class BlurMotion(Style):
    """
    Applies a motion blur effect to the image.
    """

    name = "Motion Blur"
    category = "Effects"
    parameters = [
        {
            "name": "kernel_size",
            "type": "int",
            "default": 15,
            "min": 3,
            "max": 51,
            "step": 2,
            "label": "Kernel Size",
        },
        {
            "name": "angle",
            "type": "int",
            "default": 0,
            "min": 0,
            "max": 360,
            "step": 10,
            "label": "Angle",
        },
    ]

def apply(self, image: Optional[np.ndarray], params: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """
    Apply the style to the image.
    :param image: Input BGR image.
    :param params: Dictionary of parameters.
    :return: Processed image.
    """
    if image is None:
        raise ValueError("Input image cannot be None.")

    if not isinstance(image, np.ndarray):
        raise ValueError("Invalid image provided. Expected a NumPy array.")

    # Set default parameters if params is None
    if params is None:
        params = self.default_params

    # Validate and sanitize parameters
    params = self.validate_params(params)

    kernel_size = params["kernel_size"]
    angle = params["angle"]

    # Ensure kernel size is odd
    if kernel_size % 2 == 0:
        kernel_size += 1

    # Create a horizontal kernel
    kernel = np.zeros((kernel_size, kernel_size), dtype=np.float32)
    kernel[kernel_size // 2, :] = np.ones(kernel_size)

    # Rotate the kernel to the specified angle
    center = (kernel_size / 2 - 0.5, kernel_size / 2 - 0.5)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_kernel = cv2.warpAffine(kernel, rotation_matrix, (kernel_size, kernel_size))
    rotated_kernel /= rotated_kernel.sum()  # Normalize the kernel

    # Apply the motion blur kernel to the image
    blurred_image = cv2.filter2D(image, -1, rotated_kernel)

    return blurred_image
