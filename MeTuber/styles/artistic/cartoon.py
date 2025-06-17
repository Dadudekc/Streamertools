import cv2
import numpy as np
from typing import Any, Dict, Optional
from styles.base import Style


class Cartoon(Style):
    """
    A style that applies an improved cartoon effect to the image with refined edge detection,
    bilateral filtering, and optional color quantization.
    """

    def __init__(self):
        super().__init__()
        self.name = "Cartoon"
        self.category = "Artistic"

    def define_parameters(self):
        """Define parameters for cartoon effect."""
        return {
            "bilateral_filter_diameter": {"default": 9, "min": 1, "max": 20},
            "bilateral_filter_sigmaColor": {"default": 75, "min": 1, "max": 150},
            "bilateral_filter_sigmaSpace": {"default": 75, "min": 1, "max": 150},
            "canny_threshold1": {"default": 100, "min": 0, "max": 500},
            "canny_threshold2": {"default": 200, "min": 0, "max": 500},
            "color_levels": {"default": 8, "min": 2, "max": 16}
        }

    def apply(self, image, params=None):
        """Apply cartoon effect to the image.
        
        Args:
            image (numpy.ndarray): Input image in BGR format
            params (dict, optional): Parameters for the effect
                - bilateral_filter_diameter: Diameter of the bilateral filter
                - bilateral_filter_sigmaColor: Color sigma for bilateral filter
                - bilateral_filter_sigmaSpace: Space sigma for bilateral filter
                - canny_threshold1: First threshold for edge detection
                - canny_threshold2: Second threshold for edge detection
                - color_levels: Number of color levels for quantization
        
        Returns:
            numpy.ndarray: Image with cartoon effect
        """
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Input image must be a valid NumPy array")

        # Use default parameters if none provided
        if params is None:
            params = {name: param["default"] for name, param in self.define_parameters().items()}

        # Get and validate parameters
        d = params.get("bilateral_filter_diameter", 9)
        if not 1 <= d <= 20:
            raise ValueError("Parameter 'bilateral_filter_diameter' must be between 1 and 20.")

        sigma_color = params.get("bilateral_filter_sigmaColor", 75)
        if not 1 <= sigma_color <= 150:
            raise ValueError("Parameter 'bilateral_filter_sigmaColor' must be between 1 and 150.")

        sigma_space = params.get("bilateral_filter_sigmaSpace", 75)
        if not 1 <= sigma_space <= 150:
            raise ValueError("Parameter 'bilateral_filter_sigmaSpace' must be between 1 and 150.")

        t1 = params.get("canny_threshold1", 100)
        if not 0 <= t1 <= 500:
            raise ValueError("Parameter 'canny_threshold1' must be between 0 and 500.")

        t2 = params.get("canny_threshold2", 200)
        if not 0 <= t2 <= 500:
            raise ValueError("Parameter 'canny_threshold2' must be between 0 and 500.")

        levels = params.get("color_levels", 8)
        if not 2 <= levels <= 16:
            raise ValueError("Parameter 'color_levels' must be between 2 and 16.")

        # Apply bilateral filter for smoothing while preserving edges
        color = cv2.bilateralFilter(image, d, sigma_color, sigma_space)

        # Convert to grayscale for edge detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply edge detection
        edges = cv2.Canny(gray, t1, t2)
        edges = cv2.dilate(edges, None)

        # Reduce color palette
        div = 256 // levels
        color = color // div * div + div // 2

        # Combine edges with color image
        cartoon = cv2.bitwise_and(color, color, mask=255 - edges)

        return cartoon

    def quantize_colors(self, image: np.ndarray, k: int) -> np.ndarray:
        """
        Reduces the number of colors in an image using k-means clustering.

        Args:
            image (np.ndarray): The input BGR image.
            k (int): Number of color clusters.

        Returns:
            np.ndarray: The color-quantized image.
        """
        # Reshape the image data for clustering
        data = np.float32(image).reshape((-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, centers = cv2.kmeans(
            data, k, None, criteria, 10, cv2.KMEANS_PP_CENTERS
        )
        centers = np.uint8(centers)
        quantized = centers[labels.flatten()].reshape(image.shape)
        return quantized
