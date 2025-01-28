import cv2
from styles.base import Style


class Blur(Style):
    name = "Blur"
    parameters = [
        {
            "name": "kernel_size",
            "type": "int",
            "default": 5,
            "min": 1,
            "max": 31,
            "step": 2,
            "label": "Kernel Size"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        params = self.validate_params(params)

        kernel_size = params["kernel_size"]
        if kernel_size % 2 == 0:  # Ensure kernel size is odd
            kernel_size += 1
        blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        return blurred
