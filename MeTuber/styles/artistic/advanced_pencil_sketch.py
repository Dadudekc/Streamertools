import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import logging
from styles.base import Style

class PencilSketchwithColor(Style):
    """
    A style that mimics a colored pencil drawing with a light, semi-monochrome background
    and subtle color shading.
    """
    name = "Light Pencil Sketch (Color)"
    category = "Favorites"

    parameters = [
        {
            "name": "lighten_background",
            "type": "bool",
            "default": True,
            "label": "Lighten Background",
        },
        {
            "name": "lighten_threshold",
            "type": "int",
            "default": 230,
            "min": 128,
            "max": 255,
            "step": 1,
            "label": "Background Lighten Threshold",
        },
        {
            "name": "bilateral_filter_diameter",
            "type": "int",
            "default": 7,
            "min": 1,
            "max": 20,
            "step": 1,
            "label": "Bilateral Filter Diameter",
        },
        {
            "name": "bilateral_filter_sigmaColor",
            "type": "int",
            "default": 50,
            "min": 1,
            "max": 150,
            "step": 1,
            "label": "Bilateral Filter SigmaColor",
        },
        {
            "name": "bilateral_filter_sigmaSpace",
            "type": "int",
            "default": 50,
            "min": 1,
            "max": 150,
            "step": 1,
            "label": "Bilateral Filter SigmaSpace",
        },
        {
            "name": "edge_method",
            "type": "str",
            "default": "Laplacian",
            "options": ["Canny", "Laplacian", "Sobel", "Adaptive"],
            "label": "Edge Detection Method",
        },
        {
            "name": "edge_threshold1",
            "type": "int",
            "default": 60,
            "min": 0,
            "max": 500,
            "step": 1,
            "label": "Edge Threshold 1",
        },
        {
            "name": "edge_threshold2",
            "type": "int",
            "default": 120,
            "min": 0,
            "max": 500,
            "step": 1,
            "label": "Edge Threshold 2",
        },
        {
            "name": "outline_thickness",
            "type": "int",
            "default": 1,
            "min": 1,
            "max": 5,
            "step": 1,
            "label": "Outline Thickness",
        },
        {
            "name": "posterization_levels",
            "type": "int",
            "default": 6,
            "min": 2,
            "max": 10,
            "step": 1,
            "label": "Posterization Levels",
        },
        {
            "name": "saturation_boost",
            "type": "float",
            "default": 1.0,
            "min": 0.5,
            "max": 2.0,
            "step": 0.1,
            "label": "Saturation Boost",
        },
        {
            "name": "brightness_boost",
            "type": "float",
            "default": 1.0,
            "min": 0.5,
            "max": 2.0,
            "step": 0.1,
            "label": "Brightness Boost",
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
        {
            "name": "sketch_blend",
            "type": "float",
            "default": 0.5,
            "min": 0.0,
            "max": 1.0,
            "step": 0.1,
            "label": "Sketch Influence",
        },
    ]

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

    def define_parameters(self):
        return self.parameters

    def apply(self, image, params=None):
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Input image must be a valid NumPy array.")
        if image.ndim != 3 or image.shape[2] != 3:
            raise ValueError("Input image must be a 3-channel (BGR) image.")

        params = params or {}

        lighten_bg = params.get("lighten_background", True)
        lighten_thresh = params.get("lighten_threshold", 230)
        d = params.get("bilateral_filter_diameter", 7)
        sigmaColor = params.get("bilateral_filter_sigmaColor", 50)
        sigmaSpace = params.get("bilateral_filter_sigmaSpace", 50)
        edge_method = params.get("edge_method", "Laplacian")
        threshold1 = params.get("edge_threshold1", 60)
        threshold2 = params.get("edge_threshold2", 120)
        outline_thickness = params.get("outline_thickness", 1)
        posterization_levels = params.get("posterization_levels", 6)
        saturation_boost = params.get("saturation_boost", 1.0)
        brightness_boost = params.get("brightness_boost", 1.0)
        sharpen_intensity = params.get("sharpen_intensity", 1.0)
        sketch_blend = params.get("sketch_blend", 0.5)

        # Step 1: (Optional) Lighten background
        # If you want to push near-white areas to pure white
        if lighten_bg:
            image = self.lighten_background(image, lighten_thresh)

        # Step 2: Bilateral filter to smooth color but keep edges
        filtered = cv2.bilateralFilter(image, d, sigmaColor, sigmaSpace)

        # Step 3: Edge detection
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
            # fallback
            edges = cv2.Canny(gray, threshold1, threshold2)

        # Step 4: (Optional) Thicken edges
        if outline_thickness > 1:
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (outline_thickness, outline_thickness))
            edges = cv2.dilate(edges, kernel, iterations=1)

        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        edges_colored = cv2.bitwise_not(edges_colored)

        # Step 5: Adjust color (saturation & brightness)
        color_boosted = self.adjust_color(filtered, saturation_boost, brightness_boost)

        # Step 6: Combine edges with the color image
        combined = cv2.bitwise_and(color_boosted, edges_colored)

        # Step 7: Sharpen
        sharpened = self.sharpen_image(combined, sharpen_intensity)

        # Step 8: Posterize
        final_cartoon = self.posterize_image(sharpened, posterization_levels)

        # Step 9: Create a pencil sketch from the original image
        pencil = self.create_pencil_sketch(image)

        # Step 10: Blend pencil lines with the cartoon
        # e.g. 0.5 means half pencil, half color
        out = cv2.addWeighted(final_cartoon, (1.0 - sketch_blend), pencil, sketch_blend, 0)

        return out

    def lighten_background(self, image, threshold=230):
        """
        Push near-white areas to pure white for a high-key background.
        """
        # Convert to LAB for easier lightness manipulation
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        L, A, B = cv2.split(lab)
        # Any pixel with L above some threshold becomes fully white
        # This is a naive approach, but helps push backgrounds to white.
        mask = (L > threshold)
        L[mask] = 255
        A[mask] = 128  # neutral
        B[mask] = 128  # neutral
        # Recombine
        lab = cv2.merge([L, A, B])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    def adjust_color(self, image, sat_boost, bright_boost):
        """
        Adjust saturation and brightness in HSV space.
        """
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # Multiply saturation
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * sat_boost, 0, 255)
        # Multiply value
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * bright_boost, 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def sharpen_image(self, image, intensity):
        """
        Basic sharpening using a custom kernel.
        """
        kernel = np.array([
            [0, -1, 0],
            [-1, 5 + intensity, -1],
            [0, -1, 0]
        ])
        return cv2.filter2D(image, -1, kernel)

    def posterize_image(self, image, levels=6):
        """
        Reduce color depth to create a more stylized, flat effect.
        """
        shift = 256 // levels
        posterized = (image // shift) * shift + shift // 2
        return np.clip(posterized, 0, 255).astype(np.uint8)

    def create_pencil_sketch(self, image):
        """
        Convert the original image into a grayscale pencil sketch.
        The result is BGR but mostly grayscale lines.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        inv_gray = 255 - gray
        blur = cv2.GaussianBlur(inv_gray, (21, 21), 0)
        inv_blur = 255 - blur
        sketch = cv2.divide(gray, inv_blur, scale=256.0)
        return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

