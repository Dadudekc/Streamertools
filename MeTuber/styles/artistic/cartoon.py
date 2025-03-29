import cv2
import numpy as np
from typing import Any, Dict, Optional
from styles.base import Style


class Cartoon(Style):
    """
    A style that applies an improved cartoon effect to the image with refined edge detection,
    bilateral filtering, and optional color quantization.
    """

    name = "Cartoon"
    category = "Artistic"
    parameters = [
        {
            "name": "bilateral_filter_diameter",
            "type": "int",
            "default": 9,
            "min": 1,
            "max": 20,
            "step": 1,
            "label": "Bilateral Filter Diameter",
        },
        {
            "name": "bilateral_filter_sigmaColor",
            "type": "int",
            "default": 75,
            "min": 1,
            "max": 150,
            "step": 1,
            "label": "Bilateral Filter SigmaColor",
        },
        {
            "name": "bilateral_filter_sigmaSpace",
            "type": "int",
            "default": 75,
            "min": 1,
            "max": 150,
            "step": 1,
            "label": "Bilateral Filter SigmaSpace",
        },
        {
            "name": "edge_method",
            "type": "str",
            "default": "Canny",
            "options": ["Canny", "Laplacian", "Sobel"],
            "label": "Edge Detection Method",
        },
        {
            "name": "edge_threshold1",
            "type": "int",
            "default": 100,
            "min": 0,
            "max": 500,
            "step": 1,
            "label": "Edge Threshold 1",
        },
        {
            "name": "edge_threshold2",
            "type": "int",
            "default": 200,
            "min": 0,
            "max": 500,
            "step": 1,
            "label": "Edge Threshold 2",
        },
        {
            "name": "enable_color_quantization",
            "type": "bool",
            "default": False,
            "label": "Enable Color Quantization",
        },
        {
            "name": "color_clusters",
            "type": "int",
            "default": 8,
            "min": 2,
            "max": 32,
            "step": 2,
            "label": "Color Clusters",
        },
        {
            "name": "apply_edge_dilation",
            "type": "bool",
            "default": True,
            "label": "Apply Edge Dilation",
        },
        {
            "name": "dilation_iterations",
            "type": "int",
            "default": 1,
            "min": 0,
            "max": 5,
            "step": 1,
            "label": "Dilation Iterations",
        },
    ]

    def define_parameters(self) -> list:
        """Returns the parameter definitions for the Cartoon effect."""
        return self.parameters

    def apply(self, image: np.ndarray, params: Optional[Dict[str, Any]] = None) -> np.ndarray:
        """
        Apply the cartoon effect using refined edge detection, bilateral filtering, and optional color quantization.

        Args:
            image (np.ndarray): The input image in BGR format.
            params (Optional[Dict[str, Any]]): Parameters for the cartoon effect.

        Returns:
            np.ndarray: The processed image with a cartoon effect.
        """
        # Validate image input
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Input image must be a valid NumPy array.")
        if image.ndim != 3 or image.shape[2] != 3:
            raise ValueError("Input image must be a 3-channel (BGR) image.")

        # Validate and extract parameters
        params = self.validate_params(params or {})
        d = params["bilateral_filter_diameter"]
        sigmaColor = params["bilateral_filter_sigmaColor"]
        sigmaSpace = params["bilateral_filter_sigmaSpace"]
        edge_method = params["edge_method"]
        threshold1 = params["edge_threshold1"]
        threshold2 = params["edge_threshold2"]
        enable_color_quantization = params["enable_color_quantization"]
        color_clusters = params["color_clusters"]
        apply_edge_dilation = params.get("apply_edge_dilation", True)
        dilation_iterations = params.get("dilation_iterations", 1)

        # Step 1: Apply Bilateral Filter to smooth colors while preserving edges
        filtered = cv2.bilateralFilter(image, d, sigmaColor, sigmaSpace)

        # Step 2: Convert to grayscale and apply the chosen edge detection method
        gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
        if edge_method == "Canny":
            edges = cv2.Canny(gray, threshold1, threshold2)
        elif edge_method == "Laplacian":
            edges = cv2.Laplacian(gray, cv2.CV_8U, ksize=5)
        elif edge_method == "Sobel":
            edges_x = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=5)
            edges_y = cv2.Sobel(gray, cv2.CV_8U, 0, 1, ksize=5)
            edges = cv2.addWeighted(edges_x, 0.5, edges_y, 0.5, 0)
        else:
            raise ValueError(f"Unsupported edge detection method: {edge_method}")

        # Optional: Apply dilation to thicken the edges for a more pronounced effect
        if apply_edge_dilation and dilation_iterations > 0:
            kernel = np.ones((3, 3), np.uint8)
            edges = cv2.dilate(edges, kernel, iterations=dilation_iterations)

        # Convert edge image to BGR format for later combination
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # Step 3: Optional Color Quantization for stronger cartoon effect
        if enable_color_quantization:
            quantized = self.quantize_colors(filtered, color_clusters)
        else:
            quantized = filtered

        # Step 4: Combine edges with the filtered (or quantized) image using bitwise AND
        cartoonized = cv2.bitwise_and(quantized, edges_colored)
        return cartoonized

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
