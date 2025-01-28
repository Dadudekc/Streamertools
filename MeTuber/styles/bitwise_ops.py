# MeTuber\styles\bitwise_ops.py

import abc
import cv2
import numpy as np
from .base import Style


class BitwiseOperation(Style, abc.ABC):
    """
    Abstract base class for all bitwise operations.
    Provides common functionality for generating masks and validating images.
    """
    category = "Bitwise Operations"

    def generate_mask(self, image, intensity):
        """
        Generates a mask with the given intensity.

        Args:
            image (numpy.ndarray): Input image.
            intensity (int): Intensity level for the mask.

        Returns:
            numpy.ndarray: A binary mask with the same shape as the input image.

        Raises:
            ValueError: If the input image is invalid.
        """
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Invalid image provided. Expected a NumPy array.")

        # Generate a random mask based on intensity
        mask = np.random.randint(0, 256, size=image.shape[:2], dtype=np.uint8)
        mask = cv2.threshold(mask, intensity, 255, cv2.THRESH_BINARY)[1]
        return mask

    @abc.abstractmethod
    def define_parameters(self):
        """
        Abstract method for defining parameters.
        Subclasses must implement this method.
        """
        pass


class BitwiseAnd(BitwiseOperation):
    """
    Applies a bitwise AND operation.
    """
    name = "Bitwise AND"

    def define_parameters(self):
        return [
            {
                "name": "mask_intensity",
                "type": "int",
                "default": 128,
                "min": 0,
                "max": 255,
                "step": 1,
                "label": "Mask Intensity"
            }
        ]

    def apply(self, image, params=None):
        """
        Applies a bitwise AND operation on the image.

        Args:
            image (numpy.ndarray): Input image.
            params (dict, optional): Parameters for the operation.

        Returns:
            numpy.ndarray: Image after applying the bitwise AND operation.
        """
        params = self.validate_params(params or {})
        intensity = params["mask_intensity"]
        mask = self.generate_mask(image, intensity)
        return cv2.bitwise_and(image, image, mask=mask)


class BitwiseOr(BitwiseOperation):
    """
    Applies a bitwise OR operation.
    """
    name = "Bitwise OR"

    def define_parameters(self):
        return [
            {
                "name": "mask_intensity",
                "type": "int",
                "default": 128,
                "min": 0,
                "max": 255,
                "step": 1,
                "label": "Mask Intensity"
            }
        ]

    def apply(self, image, params=None):
        """
        Applies a bitwise OR operation on the image.

        Args:
            image (numpy.ndarray): Input image.
            params (dict, optional): Parameters for the operation.

        Returns:
            numpy.ndarray: Image after applying the bitwise OR operation.
        """
        params = self.validate_params(params or {})
        intensity = params["mask_intensity"]
        mask = self.generate_mask(image, intensity)
        return cv2.bitwise_or(image, image, mask=mask)


class BitwiseXor(BitwiseOperation):
    """
    Applies a bitwise XOR operation.
    """
    name = "Bitwise XOR"

    def define_parameters(self):
        return [
            {
                "name": "mask_intensity",
                "type": "int",
                "default": 128,
                "min": 0,
                "max": 255,
                "step": 1,
                "label": "Mask Intensity"
            }
        ]

    def apply(self, image, params=None):
        """
        Applies a bitwise XOR operation on the image.

        Args:
            image (numpy.ndarray): Input image.
            params (dict, optional): Parameters for the operation.

        Returns:
            numpy.ndarray: Image after applying the bitwise XOR operation.
        """
        params = self.validate_params(params or {})
        intensity = params["mask_intensity"]
        mask = self.generate_mask(image, intensity)
        return cv2.bitwise_xor(image, image, mask=mask)
