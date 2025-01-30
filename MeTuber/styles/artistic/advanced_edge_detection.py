import cv2
import numpy as np
from ..base import Style


class AdvancedEdgeDetection(Style):
    """
    A style that applies advanced edge detection with color customization and glow effects.
    Supports Canny, Sobel, and Laplacian methods.
    """
    name = "Advanced Edge Detection"
    category = "Artistic"
    parameters = [
        {
            "name": "method",
            "type": "str",
            "default": "Canny",
            "options": ["Canny", "Sobel", "Laplacian"],
            "label": "Edge Detection Method",
        },
        {
            "name": "threshold1",
            "type": "int",
            "default": 100,
            "min": 0,
            "max": 500,
            "step": 1,
            "label": "Canny Threshold 1",
        },
        {
            "name": "threshold2",
            "type": "int",
            "default": 200,
            "min": 0,
            "max": 500,
            "step": 1,
            "label": "Canny Threshold 2",
        },
        {
            "name": "sobel_ksize",
            "type": "int",
            "default": 3,
            "min": 1,
            "max": 7,
            "step": 2,
            "label": "Sobel Kernel Size",
        },
        {
            "name": "blur",
            "type": "int",
            "default": 3,
            "min": 1,
            "max": 9,
            "step": 2,
            "label": "Pre-Processing Blur",
        },
        {
            "name": "overlay",
            "type": "bool",
            "default": True,
            "label": "Overlay Edges on Image",
        },
        {
            "name": "glow",
            "type": "bool",
            "default": True,
            "label": "Enable Glow Effect",
        },
        {
            "name": "glow_intensity",
            "type": "float",
            "default": 1.0,
            "min": 0.1,
            "max": 3.0,
            "step": 0.1,
            "label": "Glow Intensity",
        },
        {
            "name": "color_mode",
            "type": "str",
            "default": "White",
            "options": ["White", "Red", "Green", "Blue", "Custom"],
            "label": "Edge Color",
        },
        {
            "name": "custom_r",
            "type": "int",
            "default": 255,
            "min": 0,
            "max": 255,
            "step": 5,
            "label": "Custom Red (R)",
        },
        {
            "name": "custom_g",
            "type": "int",
            "default": 255,
            "min": 0,
            "max": 255,
            "step": 5,
            "label": "Custom Green (G)",
        },
        {
            "name": "custom_b",
            "type": "int",
            "default": 255,
            "min": 0,
            "max": 255,
            "step": 5,
            "label": "Custom Blue (B)",
        },
    ]

    def define_parameters(self):
        """
        Returns the parameters for edge detection.
        """
        return self.parameters

    def apply(self, image, params=None):
        if image is None:
            raise ValueError("Input image cannot be None.")
        if len(image.shape) != 3 or image.shape[2] != 3:
            raise ValueError("Input image must be a BGR color image.")

        # Validate parameters
        params = self.validate_params(params or {})
        print("Parameters received:", params)

        method = params["method"]
        threshold1 = params["threshold1"]
        threshold2 = params["threshold2"]
        sobel_ksize = params["sobel_ksize"]
        blur_ksize = params["blur"]
        overlay = params["overlay"]
        glow_enabled = params["glow"]
        glow_intensity = params["glow_intensity"]
        color_mode = params["color_mode"]
        custom_r = params["custom_r"]
        custom_g = params["custom_g"]
        custom_b = params["custom_b"]

        # Debugging: Check color_mode
        if color_mode not in ["White", "Red", "Green", "Blue", "Custom"]:
            print(f"Invalid color_mode detected: {color_mode}. Defaulting to White.")
            color_mode = "White"
        else:
            print(f"Valid color_mode detected: {color_mode}.")

        # Ensure blur kernel size is always odd
        if blur_ksize % 2 == 0:
            blur_ksize += 1

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur
        if blur_ksize > 1:
            gray = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)

        # Apply edge detection
        if method == "Canny":
            edges = cv2.Canny(gray, threshold1, threshold2)
        elif method == "Sobel":
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_ksize)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_ksize)
            edges = cv2.magnitude(sobelx, sobely)
            edges = cv2.normalize(edges, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        elif method == "Laplacian":
            edges = cv2.Laplacian(gray, cv2.CV_64F, ksize=sobel_ksize)
            edges = cv2.convertScaleAbs(edges)
        else:
            raise ValueError(f"Unknown edge detection method: {method}")

        # Create edge mask
        edge_mask = edges > 0
        print(f"Edge mask created. Total edge pixels: {np.sum(edge_mask)}")

        # Initialize blank color image for edges
        edges_colored = np.zeros_like(image)

        # Set edge color based on color_mode
        if color_mode == "White":
            color = (255, 255, 255)
        elif color_mode == "Red":
            color = (0, 0, 255)
        elif color_mode == "Green":
            color = (0, 255, 0)
        elif color_mode == "Blue":
            color = (255, 0, 0)
        elif color_mode == "Custom":
            print(f"Custom color values: R={custom_r}, G={custom_g}, B={custom_b}")
            if not (0 <= custom_r <= 255 and 0 <= custom_g <= 255 and 0 <= custom_b <= 255):
                print("Invalid custom RGB values, defaulting to white.")
                color = (255, 255, 255)
            else:
                color = (custom_b, custom_g, custom_r)
                print(f"Custom color applied: {color}")
        else:
            color = (255, 255, 255)

        # Apply color to edges
        print(f"Applying color: {color} to {np.sum(edge_mask)} edge pixels.")
        edges_colored[edge_mask] = color

        # Apply glow effect
        if glow_enabled:
            glow = cv2.GaussianBlur(edges_colored, (15, 15), sigmaX=glow_intensity * 3)
            edges_colored = cv2.addWeighted(edges_colored, 1.0, glow, glow_intensity, 0)
            print("Glow effect applied.")

        # Overlay edges on the original image if needed
        if overlay:
            combined = cv2.addWeighted(image, 0.7, edges_colored, 0.3, 0)
            return combined
        else:
            return edges_colored
