import cv2
import numpy as np
from .base import Style


class BitwiseOperation(Style):
    """
    Base class for all bitwise operations.
    """
    category = "Bitwise Operations"

    def generate_mask(self, image, intensity):
        """
        Generates a mask with the given intensity.
        """
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Invalid image provided. Expected a NumPy array.")
        
        # Example mask generation logic to ensure variation
        mask = np.random.randint(0, intensity, size=image.shape[:2], dtype=np.uint8)
        return mask

class BitwiseAnd(BitwiseOperation):
    """
    Applies a bitwise AND operation.
    """
    name = "Bitwise AND"
    parameters = [
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
        if params is None:
            params = {}
        params = self.validate_params(params)
        intensity = params["mask_intensity"]

        mask = self.generate_mask(image, intensity)
        return cv2.bitwise_and(image, image, mask=mask)


class BitwiseOr(BitwiseOperation):
    """
    Applies a bitwise OR operation.
    """
    name = "Bitwise OR"
    parameters = [
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
        if params is None:
            params = {}
        params = self.validate_params(params)
        intensity = params["mask_intensity"]

        mask = self.generate_mask(image, intensity)
        return cv2.bitwise_or(image, image, mask=mask)


class BitwiseXor(BitwiseOperation):
    """
    Applies a bitwise XOR operation.
    """
    name = "Bitwise XOR"
    parameters = [
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
        if params is None:
            params = {}
        params = self.validate_params(params)
        intensity = params["mask_intensity"]

        mask = self.generate_mask(image, intensity)
        return cv2.bitwise_xor(image, image, mask=mask)
