import cv2
import numpy as np
import logging
from styles.base import Style

class CartoonWholeImage(Style):
    """
    A style that applies a cartoon/illustration effect across the entire image.
    This pipeline does not preserve the face as normal; everything is stylized.
    """
    name = "Cartoon Whole Image"
    category = "Favorites"

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
            "name": "enable_color_quantization",
            "type": "bool",
            "default": True,
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
            "name": "edge_method",
            "type": "str",
            "default": "Laplacian",
            "options": ["Canny", "Laplacian", "Sobel"],
            "label": "Edge Detection Method",
        },
        {
            "name": "edge_threshold1",
            "type": "int",
            "default": 80,
            "min": 0,
            "max": 500,
            "step": 1,
            "label": "Edge Threshold 1",
        },
        {
            "name": "edge_threshold2",
            "type": "int",
            "default": 160,
            "min": 0,
            "max": 500,
            "step": 1,
            "label": "Edge Threshold 2",
        },
        {
            "name": "edge_thickness",
            "type": "int",
            "default": 1,
            "min": 1,
            "max": 5,
            "step": 1,
            "label": "Edge Thickness (Dilation)",
        },
        {
            "name": "sharpen_intensity",
            "type": "float",
            "default": 1.0,
            "min": 0.0,
            "max": 3.0,
            "step": 0.1,
            "label": "Sharpen Intensity",
        },
    ]

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

    def define_parameters(self):
        return self.parameters

    def apply(self, image, params=None):
        """
        Apply a cartoon/illustration effect to the entire image:
        1) Bilateral filter for color smoothing
        2) (Optional) Color quantization
        3) Edge detection + thickening
        4) Combine edges with color
        """
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Input image must be a valid NumPy array.")
        if image.ndim != 3 or image.shape[2] != 3:
            raise ValueError("Input image must be a 3-channel (BGR) image.")

        params = params or {}
        d = params.get("bilateral_filter_diameter", 9)
        sigmaColor = params.get("bilateral_filter_sigmaColor", 75)
        sigmaSpace = params.get("bilateral_filter_sigmaSpace", 75)
        enable_color_quant = params.get("enable_color_quantization", True)
        color_clusters = params.get("color_clusters", 8)
        edge_method = params.get("edge_method", "Laplacian")
        t1 = params.get("edge_threshold1", 80)
        t2 = params.get("edge_threshold2", 160)
        thickness = params.get("edge_thickness", 1)
        sharpen_intensity = params.get("sharpen_intensity", 1.0)

        # 1) Bilateral filter to smooth colors while preserving edges
        smoothed = cv2.bilateralFilter(image, d, sigmaColor, sigmaSpace)

        # 2) (Optional) Color quantization to reduce color detail
        if enable_color_quant:
            color_reduced = self.quantize_colors(smoothed, color_clusters)
        else:
            color_reduced = smoothed

        # 3) Edge detection
        edges = self.detect_edges(smoothed, edge_method, t1, t2)

        # 4) (Optional) Thicken edges
        if thickness > 1:
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (thickness, thickness))
            edges = cv2.dilate(edges, kernel, iterations=1)

        # Invert edges
        edges_inv = cv2.bitwise_not(cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR))

        # 5) Combine edges with color
        cartoon = cv2.bitwise_and(color_reduced, edges_inv)

        # 6) (Optional) Sharpen the final image
        cartoon_sharp = self.sharpen_image(cartoon, sharpen_intensity)

        return cartoon_sharp

    # ----------------------------------
    # HELPER METHODS
    # ----------------------------------

    def quantize_colors(self, image, k):
        """Use k-means to reduce color palette."""
        data = np.float32(image).reshape(-1, 3)
        _, labels, centers = cv2.kmeans(
            data, k, None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0),
            10, cv2.KMEANS_RANDOM_CENTERS
        )
        centers = np.uint8(centers)
        quantized = centers[labels.flatten()].reshape(image.shape)
        return quantized

    def detect_edges(self, image, method, t1, t2):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if method == "Canny":
            edges = cv2.Canny(gray, t1, t2)
        elif method == "Laplacian":
            edges = cv2.Laplacian(gray, cv2.CV_8U, ksize=5)
        elif method == "Sobel":
            edges_x = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=5)
            edges_y = cv2.Sobel(gray, cv2.CV_8U, 0, 1, ksize=5)
            edges = cv2.addWeighted(edges_x, 0.5, edges_y, 0.5, 0)
        else:
            edges = cv2.Canny(gray, t1, t2)
        return edges

    def sharpen_image(self, image, intensity):
        """Sharpen using a custom kernel."""
        kernel = np.array([
            [0, -1, 0],
            [-1, 5 + intensity, -1],
            [0, -1, 0]
        ])
        return cv2.filter2D(image, -1, kernel)
