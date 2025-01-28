import cv2
import numpy as np
from ..base import Style


class GlowingEdges(Style):
    """
    Enhances edges in the image and adds a glowing effect.
    """

    name = "Glowing Edges"
    category = "Effects"
    parameters = [
        {
            "name": "edge_threshold",
            "type": "int",
            "default": 100,
            "min": 0,
            "max": 300,
            "step": 10,
            "label": "Edge Threshold",
        },
        {
            "name": "blur_size",
            "type": "int",
            "default": 7,
            "min": 1,
            "max": 21,
            "step": 2,
            "label": "Blur Size",
        },
    ]

    def define_parameters(self):
        """
        Define the parameters for this style.
        Returns:
            list: List of parameter dictionaries.
        """
        return self.parameters

    def apply(self, image, params=None):
        """
        Enhances edges and adds a glowing effect by blending the original image with blurred edges.

        Args:
            image (numpy.ndarray): The input image in BGR format.
            params (dict, optional): Parameters for glowing edges.

        Returns:
            numpy.ndarray: The image with glowing edges effect.

        Raises:
            ValueError: If the input image is None or invalid.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")

        # Validate and sanitize parameters
        params = self.validate_params(params)

        edge_threshold = params["edge_threshold"]
        blur_size = params["blur_size"]

        # Ensure blur size is odd (required by GaussianBlur)
        if blur_size % 2 == 0:
            blur_size += 1

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect edges using the Canny edge detector
        edges = cv2.Canny(gray, edge_threshold, edge_threshold * 2)

        # Convert edges back to BGR format
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # Apply Gaussian blur to soften the edges
        blurred_edges = cv2.GaussianBlur(edges_bgr, (blur_size, blur_size), 0)

        # Blend the blurred edges with the original image
        glowing_image = cv2.addWeighted(image, 0.8, blurred_edges, 0.2, 0)

        return glowing_image
