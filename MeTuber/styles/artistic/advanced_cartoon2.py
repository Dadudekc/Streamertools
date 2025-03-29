import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import logging
from styles.base import Style  # Ensure it's correctly imported

class AdvancedCartoonAnime(Style):  # Inherits from Style
    """
    An extended style that applies a stylized anime/isekai effect by enhancing edges,
    boosting colors, posterizing the image, and optionally applying bloom and texture overlays.
    """
    name = "Advanced Cartoon (Anime)"
    category = "Favorites"
    parameters = [
        {
            "name": "anime_mode",
            "type": "bool",
            "default": True,
            "label": "Enable Anime Mode",
        },
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
            "default": "Laplacian",
            "options": ["Canny", "Laplacian", "Sobel", "Adaptive"],
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
            "name": "outline_thickness",
            "type": "int",
            "default": 2,
            "min": 1,
            "max": 5,
            "step": 1,
            "label": "Outline Thickness",
        },
        {
            "name": "posterization_levels",
            "type": "int",
            "default": 4,
            "min": 2,
            "max": 10,
            "step": 1,
            "label": "Posterization Levels",
        },
        {
            "name": "saturation_boost",
            "type": "float",
            "default": 1.4,
            "min": 1.0,
            "max": 2.0,
            "step": 0.1,
            "label": "Saturation Boost",
        },
        {
            "name": "brightness_boost",
            "type": "float",
            "default": 1.1,
            "min": 1.0,
            "max": 2.0,
            "step": 0.1,
            "label": "Brightness Boost",
        },
        {
            "name": "sharpen_intensity",
            "type": "float",
            "default": 1.8,
            "min": 0.0,
            "max": 3.0,
            "step": 0.1,
            "label": "Sharpen Intensity",
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
            "name": "enable_dynamic_lighting",
            "type": "bool",
            "default": True,
            "label": "Enable Dynamic Lighting",
        },
        {
            "name": "enable_bloom_effect",
            "type": "bool",
            "default": True,
            "label": "Enable Bloom Effect",
        },
        {
            "name": "bloom_intensity",
            "type": "float",
            "default": 0.4,
            "min": 0.1,
            "max": 1.0,
            "step": 0.1,
            "label": "Bloom Intensity",
        },
        # You can add texture overlay parameters here if needed.
    ]

    def __init__(self):
        super().__init__()  # Call the base class constructor
        self.logger = logging.getLogger(self.__class__.__name__)
        self.texture_loaded = False
        self.texture = None
        self.texture_colored = None

    def define_parameters(self):
        """
        Returns the parameter definitions for the Advanced Cartoon (Anime) effect.
        This is used by the GUI to generate control widgets.
        """
        return self.parameters

    def apply(self, image, params=None):
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Input image must be a valid NumPy array.")
        if image.ndim != 3 or image.shape[2] != 3:
            raise ValueError("Input image must be a 3-channel (BGR) image.")

        # Retrieve parameters (or use defaults)
        params = params or {}
        d = params.get("bilateral_filter_diameter", 9)
        sigmaColor = params.get("bilateral_filter_sigmaColor", 75)
        sigmaSpace = params.get("bilateral_filter_sigmaSpace", 75)
        edge_method = params.get("edge_method", "Laplacian")
        threshold1 = params.get("edge_threshold1", 80)
        threshold2 = params.get("edge_threshold2", 160)
        outline_thickness = params.get("outline_thickness", 2)
        posterization_levels = params.get("posterization_levels", 4)
        saturation_boost = params.get("saturation_boost", 1.4)
        brightness_boost = params.get("brightness_boost", 1.1)
        sharpen_intensity = params.get("sharpen_intensity", 1.8)
        enable_color_quantization = params.get("enable_color_quantization", True)
        color_clusters = params.get("color_clusters", 8)
        enable_dynamic_lighting = params.get("enable_dynamic_lighting", True)
        enable_texture_overlay = params.get("enable_texture_overlay", False)
        texture_path = params.get("texture_path", "textures/texture.png")
        texture_alpha = params.get("texture_alpha", 0.2)
        custom_color_palette = params.get("custom_color_palette", True)
        color_palette = params.get("color_palette", "vibrant")
        enable_bloom_effect = params.get("enable_bloom_effect", True)
        bloom_intensity = params.get("bloom_intensity", 0.4)
        anime_mode = params.get("anime_mode", True)

        # 1) Apply bilateral filter for smoothing
        filtered = cv2.bilateralFilter(image, d, sigmaColor, sigmaSpace)

        # 2) Edge detection on the smoothed grayscale image
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
            edges = cv2.Canny(gray, threshold1, threshold2)

        # If anime mode is enabled, thicken edges using morphological dilation
        if anime_mode:
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (outline_thickness, outline_thickness))
            edges = cv2.dilate(edges, kernel, iterations=1)

        # Convert edges to BGR and invert colors
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        edges_colored = cv2.bitwise_not(edges_colored)

        # 3) Optionally apply color quantization
        if enable_color_quantization:
            quantized = self.quantize_colors(filtered, color_clusters)
        else:
            quantized = filtered

        # 4) Apply custom color palette adjustments if enabled
        if custom_color_palette:
            quantized = self.apply_color_palette(quantized, color_palette)

        # 5) Boost saturation and brightness for an enhanced anime look
        if anime_mode:
            quantized = self.boost_anime_colors(quantized, saturation_boost, brightness_boost)

        # 6) Combine edges with the quantized image
        cartoon = cv2.bitwise_and(quantized, edges_colored)

        # 7) Sharpen the combined image for extra clarity
        sharpened = self.sharpen_image(cartoon, sharpen_intensity)

        # 8) Posterize the image for a cel-shaded effect
        if anime_mode:
            sharpened = self.posterize_image(sharpened, levels=posterization_levels)

        # 9) Optionally apply a bloom effect
        if anime_mode and enable_bloom_effect:
            sharpened = self.apply_bloom(sharpened, bloom_intensity)

        # 10) Optionally overlay a texture
        if enable_texture_overlay:
            sharpened = self.apply_texture(sharpened, texture_path, texture_alpha)

        return sharpened

    def quantize_colors(self, image, k):
        """Apply k-means color quantization."""
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
        """Apply a predefined color palette adjustment."""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        if palette == "vibrant":
            hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.2, 0, 255)
            hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.1, 0, 255)
        elif palette == "muted":
            hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 0.7, 0, 255)
            hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 0.9, 0, 255)
        elif palette == "monochrome":
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def boost_anime_colors(self, image, saturation_boost, brightness_boost):
        """Enhance saturation and brightness for a more vivid anime look."""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation_boost, 0, 255)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * brightness_boost, 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def sharpen_image(self, image, intensity):
        """Sharpen the image using a custom kernel."""
        kernel = np.array([
            [0, -1, 0],
            [-1, 5 + intensity, -1],
            [0, -1, 0]
        ])
        return cv2.filter2D(image, -1, kernel)

    def posterize_image(self, image, levels=4):
        """Reduce color depth to create a cel-shaded effect."""
        shift = 256 // levels
        posterized = (image // shift) * shift + shift // 2
        return np.clip(posterized, 0, 255).astype(np.uint8)

    def apply_bloom(self, image, intensity):
        """Apply a bloom effect to bright areas."""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        v = hsv[:, :, 2]
        blurred = cv2.GaussianBlur(v, (0, 0), intensity * 10)
        hsv[:, :, 2] = cv2.addWeighted(v, 1.0, blurred, intensity, 0)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def apply_texture(self, image, texture_path, alpha):
        """Overlay a texture onto the image."""
        if not self.texture_loaded:
            self.texture = cv2.imread(texture_path, cv2.IMREAD_GRAYSCALE)
            if self.texture is None:
                self.logger.warning(f"Texture file '{texture_path}' not found. Skipping texture overlay.")
            else:
                self.texture = cv2.resize(self.texture, (image.shape[1], image.shape[0]))
                self.texture_colored = cv2.applyColorMap(self.texture, cv2.COLORMAP_BONE)
            self.texture_loaded = True
        if self.texture is not None:
            blended = cv2.addWeighted(image, 1 - alpha, self.texture_colored, alpha, 0)
            return blended
        return image
