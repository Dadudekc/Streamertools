import cv2
import numpy as np
from styles.base import Style


class Halftone(Style):
    """
    Applies a halftone effect to the image with adjustable dot size and threshold.
    """

    def __init__(self):
        super().__init__()
        self.name = "Halftone"
        self.category = "Distortions"

    def define_parameters(self):
        """
        Defines the parameters for the Halftone effect.

        Returns:
            dict: Dictionary of parameter names and their default values.
        """
        return {
            "dot_size": {"default": 3, "min": 1, "max": 10},
            "threshold": {"default": 128, "min": 0, "max": 255}
        }

    def apply(self, image, params=None):
        """
        Applies a halftone effect by thresholding and adding dot patterns.

        Args:
            image (numpy.ndarray): The input image in BGR format.
            params (dict, optional): Parameters for halftone effect.

        Returns:
            numpy.ndarray: The image with a halftone effect.

        Raises:
            ValueError: If the input image is None or invalid.
        """
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Input image must be a valid NumPy array")

        # Use default parameters if none provided
        if params is None:
            params = {name: param["default"] for name, param in self.define_parameters().items()}

        # Get and validate parameters
        dot_size = params.get("dot_size", 3)
        if not 1 <= dot_size <= 10:
            raise ValueError("Parameter 'dot_size' must be between 1 and 10.")

        threshold = params.get("threshold", 128)
        if not 0 <= threshold <= 255:
            raise ValueError("Parameter 'threshold' must be between 0 and 255.")

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Create output image
        output = np.zeros_like(image)

        # Process each color channel separately
        for c in range(3):
            # Get current channel
            channel = image[:, :, c]
            
            # Create halftone pattern for this channel
            for y in range(0, gray.shape[0], dot_size):
                for x in range(0, gray.shape[1], dot_size):
                    # Get the average intensity in this region
                    region = channel[y:y+dot_size, x:x+dot_size]
                    avg_intensity = np.mean(region)
                    
                    # Create dot based on intensity
                    if avg_intensity > threshold:
                        output[y:y+dot_size, x:x+dot_size, c] = 255
                    else:
                        output[y:y+dot_size, x:x+dot_size, c] = 0

        return output
