# D:\MeTuber\MeTuber\styles\artistic\advanced_cartoon.py

import cv2
import numpy as np
from styles.base import Style
from sklearn.model_selection import ParameterGrid
from sklearn.metrics import mean_squared_error
import logging

# Ensure scikit-image is installed for advanced metrics if needed
# pip install scikit-image
from skimage.metrics import structural_similarity as ssim


class AdvancedCartoon(Style):
    """
    A style that applies an advanced cartoon effect to the image with refined edge detection,
    smoothing, optional color quantization, dynamic lighting, texture overlays, and AI-assisted
    parameter optimization.
    """

    name = "Advanced Cartoon"
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
            "name": "edge_method",
            "type": "str",
            "default": "Canny",
            "options": ["Canny", "Laplacian", "Sobel", "Adaptive"],
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
            "name": "sharpen_intensity",
            "type": "float",
            "default": 1.5,
            "min": 0.0,
            "max": 3.0,
            "step": 0.1,
            "label": "Sharpen Intensity",
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
            "name": "enable_dynamic_lighting",
            "type": "bool",
            "default": False,
            "label": "Enable Dynamic Lighting",
        },
        {
            "name": "enable_texture_overlay",
            "type": "bool",
            "default": False,
            "label": "Enable Texture Overlay",
        },
        {
            "name": "texture_path",
            "type": "file",
            "default": "textures/texture.png",
            "label": "Texture Image Path",
            "file_filter": "Image Files (*.png *.jpg *.jpeg *.bmp)"
        },
        {
            "name": "texture_alpha",
            "type": "float",
            "default": 0.2,
            "min": 0.0,
            "max": 1.0,
            "step": 0.05,
            "label": "Texture Alpha",
        },
        {
            "name": "custom_color_palette",
            "type": "bool",
            "default": False,
            "label": "Use Custom Color Palette",
        },
        {
            "name": "color_palette",
            "type": "str",
            "default": "vibrant",
            "options": ["vibrant", "muted", "monochrome"],
            "label": "Color Palette",
        },
        {
            "name": "enable_ai_optimization",
            "type": "bool",
            "default": False,
            "label": "Enable AI Parameter Optimization",
        },
    ]

    def __init__(self):
        super().__init__()
        self.texture_loaded = False  # Cache status
        self.texture = None
        self.texture_colored = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def define_parameters(self):
        """
        Returns the parameter definitions for the Advanced Cartoon effect.
        """
        return self.parameters

    def apply(self, image, params=None):
        """
        Apply the advanced cartoon effect using refined edge detection, smoothing,
        optional color quantization, dynamic lighting, texture overlays, and AI-assisted
        parameter optimization.

        Args:
            image (numpy.ndarray): The input image in BGR format.
            params (dict, optional): Parameters for the cartoon effect.

        Returns:
            numpy.ndarray: The processed image with a cartoon effect.
        """
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Input image must be a valid NumPy array.")
        if image.ndim != 3 or image.shape[2] != 3:
            raise ValueError("Input image must be a 3-channel (BGR) image.")

        # Validate and retrieve parameters
        params = self.validate_params(params or {})

        # Extract validated parameters
        d = params["bilateral_filter_diameter"]
        sigmaColor = params["bilateral_filter_sigmaColor"]
        sigmaSpace = params["bilateral_filter_sigmaSpace"]
        edge_method = params["edge_method"]
        threshold1 = params["edge_threshold1"]
        threshold2 = params["edge_threshold2"]
        sharpen_intensity = params["sharpen_intensity"]
        enable_color_quantization = params["enable_color_quantization"]
        color_clusters = params["color_clusters"]
        enable_dynamic_lighting = params["enable_dynamic_lighting"]
        enable_texture_overlay = params["enable_texture_overlay"]
        texture_path = params["texture_path"]
        texture_alpha = params["texture_alpha"]
        custom_color_palette = params["custom_color_palette"]
        color_palette = params["color_palette"]
        enable_ai_optimization = params["enable_ai_optimization"]

        # Optional: AI-Assisted Parameter Optimization
        if enable_ai_optimization:
            self.logger.info("Starting AI-assisted parameter optimization.")
            params = self.ai_optimize(image, params)
            # Re-extract parameters after optimization
            d = params["bilateral_filter_diameter"]
            sigmaColor = params["bilateral_filter_sigmaColor"]
            sigmaSpace = params["bilateral_filter_sigmaSpace"]
            edge_method = params["edge_method"]
            threshold1 = params["edge_threshold1"]
            threshold2 = params["edge_threshold2"]
            sharpen_intensity = params["sharpen_intensity"]
            enable_color_quantization = params["enable_color_quantization"]
            color_clusters = params["color_clusters"]
            enable_dynamic_lighting = params["enable_dynamic_lighting"]
            enable_texture_overlay = params["enable_texture_overlay"]
            texture_path = params["texture_path"]
            texture_alpha = params["texture_alpha"]
            custom_color_palette = params["custom_color_palette"]
            color_palette = params["color_palette"]

        # Step 1: Apply Bilateral Filter to smooth colors while preserving edges
        filtered = cv2.bilateralFilter(image, d, sigmaColor, sigmaSpace)

        # Step 2: Convert to grayscale and apply chosen edge detection method
        gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)

        if edge_method == "Canny":
            edges = cv2.Canny(gray, threshold1, threshold2)
        elif edge_method == "Laplacian":
            edges = cv2.Laplacian(gray, cv2.CV_8U, ksize=5)
        elif edge_method == "Sobel":
            edges_x = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=5)
            edges_y = cv2.Sobel(gray, cv2.CV_8U, 0, 1, ksize=5)
            edges = cv2.addWeighted(edges_x, 0.5, edges_y, 0.5, 0)
        elif edge_method == "Adaptive":
            edges = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2
            )
        else:
            raise ValueError("Unsupported edge detection method.")

        # Convert edges to BGR and invert
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        edges_colored = cv2.bitwise_not(edges_colored)

        # Step 3: Optional Color Quantization for stronger cartoon effect
        if enable_color_quantization:
            quantized = self.quantize_colors(filtered, color_clusters)
        else:
            quantized = filtered

        # Step 4: Optional Custom Color Palette
        if custom_color_palette:
            quantized = self.apply_color_palette(quantized, color_palette)

        # Step 5: Combine edges with the quantized image
        cartoon = cv2.bitwise_and(quantized, edges_colored)

        # Step 6: Optional Dynamic Lighting and Shadowing
        if enable_dynamic_lighting:
            cartoon = self.dynamic_lighting(cartoon)

        # Step 7: Sharpening the image for better definition
        sharpened = self.sharpen_image(cartoon, sharpen_intensity)

        # Step 8: Optional Texture Overlay
        if enable_texture_overlay:
            sharpened = self.apply_texture(sharpened, texture_path, texture_alpha)

        return sharpened

    def quantize_colors(self, image, k):
        """
        Reduces the number of colors in an image using k-means clustering.

        Args:
            image (numpy.ndarray): The input BGR image.
            k (int): Number of color clusters.

        Returns:
            numpy.ndarray: The color-quantized image.
        """
        data = np.float32(image).reshape(-1, 3)
        _, labels, centers = cv2.kmeans(
            data,
            k,
            None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0),
            10,
            cv2.KMEANS_RANDOM_CENTERS,
        )
        centers = np.uint8(centers)
        quantized = centers[labels.flatten()].reshape(image.shape)
        return quantized

    def apply_color_palette(self, image, palette):
        """
        Applies a predefined color palette to the image.

        Args:
            image (numpy.ndarray): The input BGR image.
            palette (str): The name of the color palette to apply.

        Returns:
            numpy.ndarray: The image with the applied color palette.
        """
        if palette == "vibrant":
            # Example vibrant palette adjustment
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            hsv[:, :, 1] = cv2.multiply(hsv[:, :, 1], 1.2)  # Increase saturation
            hsv[:, :, 2] = cv2.multiply(hsv[:, :, 2], 1.1)  # Increase brightness
            hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
            hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)
            return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        elif palette == "muted":
            # Example muted palette adjustment
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            hsv[:, :, 1] = cv2.multiply(hsv[:, :, 1], 0.7)  # Decrease saturation
            hsv[:, :, 2] = cv2.multiply(hsv[:, :, 2], 0.9)  # Decrease brightness
            hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
            hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)
            return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        elif palette == "monochrome":
            # Convert to grayscale and back to BGR
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        else:
            raise ValueError("Unsupported color palette.")

    def dynamic_lighting(self, image):
        """
        Enhances dynamic lighting and shadowing to add depth to the image.

        Args:
            image (numpy.ndarray): The input BGR image.

        Returns:
            numpy.ndarray: The image with enhanced lighting.
        """
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # Equalize the histogram of the V channel (brightness)
        hsv[:, :, 2] = cv2.equalizeHist(hsv[:, :, 2])
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def sharpen_image(self, image, intensity):
        """
        Sharpens the image to enhance fine details.

        Args:
            image (numpy.ndarray): The input BGR image.
            intensity (float): The intensity of sharpening.

        Returns:
            numpy.ndarray: The sharpened image.
        """
        kernel = np.array(
            [
                [0, -1, 0],
                [-1, 5 + intensity, -1],
                [0, -1, 0],
            ]
        )
        return cv2.filter2D(image, -1, kernel)

    def apply_texture(self, image, texture_path, alpha):
        """
        Applies a subtle texture overlay to emulate traditional comic book textures.

        Args:
            image (numpy.ndarray): The input BGR image.
            texture_path (str): Path to the texture image.
            alpha (float): Transparency factor for the texture overlay.

        Returns:
            numpy.ndarray: The image with texture overlay.
        """
        if not self.texture_loaded:
            self.texture = cv2.imread(texture_path, cv2.IMREAD_GRAYSCALE)
            if self.texture is None:
                self.logger.warning(f"Texture file '{texture_path}' not found. Skipping texture overlay.")
            else:
                self.texture = cv2.resize(self.texture, (image.shape[1], image.shape[0]))
                self.texture_colored = cv2.applyColorMap(self.texture, cv2.COLORMAP_BONE)
            self.texture_loaded = True  # Update cache

        if self.texture is not None:
            blended = cv2.addWeighted(image, 1 - alpha, self.texture_colored, alpha, 0)
            return blended
        else:
            return image

    def ai_optimize(self, image, current_params):
        """
        AI-Assisted Parameter Optimization using Grid Search to find optimal parameters
        that maximize the Structural Similarity Index (SSIM) between the original and processed images.

        Args:
            image (numpy.ndarray): The input BGR image.
            current_params (dict): Current parameters for processing.

        Returns:
            dict: Optimized parameters.
        """
        self.logger.info("Starting AI-assisted parameter optimization.")

        # Define a limited parameter grid for computational efficiency
        params_grid = {
            "bilateral_filter_diameter": [5, 9],
            "bilateral_filter_sigmaColor": [75, 100],
            "bilateral_filter_sigmaSpace": [75, 100],
            "edge_method": ["Canny", "Sobel"],
            "edge_threshold1": [50, 100],
            "edge_threshold2": [150, 200],
            "enable_color_quantization": [True, False],
            "color_clusters": [8, 16],
            "enable_dynamic_lighting": [True, False],
            "enable_texture_overlay": [False, True],
            "texture_alpha": [0.1, 0.2],
            "custom_color_palette": [True, False],
            "color_palette": ["vibrant", "muted"],
        }

        best_params = current_params.copy()
        best_score = -1  # SSIM ranges from -1 to 1

        for params in ParameterGrid(params_grid):
            try:
                processed = self.apply(image, params)
                # Convert images to grayscale for SSIM
                image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                processed_gray = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
                score = ssim(image_gray, processed_gray)
                if score > best_score:
                    best_score = score
                    best_params = params
            except Exception as e:
                # Skip parameter sets that cause errors
                self.logger.error(f"Skipping parameter set due to error: {e}")
                continue

        self.logger.info("AI Optimization Complete. Best Parameters Found:")
        for key, value in best_params.items():
            self.logger.info(f"  {key}: {value}")

        return best_params
