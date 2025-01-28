# styles/effects/misc/color_quantization.py

import cv2
import numpy as np
from ..base import Style


class ColorQuantization(Style):
    """
    Reduces the number of colors in the image using k-means clustering.
    """

    name = "Color Quantization"
    category = "Effects"
    parameters = [
        {
            "name": "clusters",
            "type": "int",
            "default": 8,
            "min": 2,
            "max": 32,
            "step": 1,
            "label": "Clusters",
        }
    ]

    def apply(self, image, params=None):
        """
        Reduces the number of colors in the image using k-means clustering.

        Args:
            image (numpy.ndarray): The input image in BGR format.
            params (dict, optional): Parameters for color quantization.

        Returns:
            numpy.ndarray: The color-quantized image.

        Raises:
            ValueError: If the input image is None or invalid.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")

        # Validate and sanitize parameters
        params = self.validate_params(params)

        clusters = params["clusters"]

        # Reshape the image to a 2D array of pixels and 3 color values (BGR)
        Z = image.reshape((-1, 3)).astype(np.float32)

        # Define criteria, number of clusters (K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        attempts = 10
        ret, labels, centers = cv2.kmeans(Z, clusters, None, criteria, attempts, cv2.KMEANS_RANDOM_CENTERS)

        # Convert centers to uint8 (as required by OpenCV)
        centers = np.uint8(centers)

        # Map each pixel to the center value
        res = centers[labels.flatten()]

        # Reshape back to the original image dimension
        quantized = res.reshape((image.shape))

        return quantized
