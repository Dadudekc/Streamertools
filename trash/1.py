# styles.py

import cv2
import numpy as np

class Style:
    """
    Base class for all styles.
    """
    name = "Base Style"
    parameters = []

    def apply(self, image, params=None):
        """
        Apply the style to the image.
        :param image: Input BGR image.
        :param params: Dictionary of parameters.
        :return: Processed image.
        """
        return image

class PencilSketch(Style):
    name = "Pencil Sketch"
    parameters = [
        {
            "name": "blur_intensity",
            "type": "int",
            "default": 21,
            "min": 1,
            "max": 51,
            "step": 2,
            "label": "Blur Intensity"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        blur_intensity = params.get("blur_intensity", 21)
        # Ensure blur intensity is odd
        if blur_intensity % 2 == 0:
            blur_intensity += 1
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        inverted_gray = cv2.bitwise_not(gray)
        blurred = cv2.GaussianBlur(inverted_gray, (blur_intensity, blur_intensity), 0)
        inverted_blur = cv2.bitwise_not(blurred)
        sketch = cv2.divide(gray, inverted_blur, scale=256.0)
        return sketch

class Grayscale(Style):
    name = "Grayscale"
    parameters = []

    def apply(self, image, params=None):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

class Original(Style):
    name = "Original"
    parameters = []

    def apply(self, image, params=None):
        return image

class Sepia(Style):
    name = "Sepia"
    parameters = [
        {
            "name": "sepia_intensity",
            "type": "float",
            "default": 1.0,
            "min": 0.0,
            "max": 2.0,
            "step": 0.1,
            "label": "Sepia Intensity"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        intensity = params.get("sepia_intensity", 1.0)
        sepia_filter = np.array([[0.272, 0.534, 0.131],
                                 [0.349, 0.686, 0.168],
                                 [0.393, 0.769, 0.189]])
        sepia_image = cv2.transform(image, sepia_filter)
        sepia_image = np.clip(sepia_image * intensity, 0, 255).astype(np.uint8)
        return sepia_image

class EdgeDetection(Style):
    name = "Edge Detection"
    parameters = [
        {
            "name": "threshold1",
            "type": "int",
            "default": 100,
            "min": 0,
            "max": 500,
            "step": 1,
            "label": "Threshold 1"
        },
        {
            "name": "threshold2",
            "type": "int",
            "default": 200,
            "min": 0,
            "max": 500,
            "step": 1,
            "label": "Threshold 2"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        threshold1 = params.get("threshold1", 100)
        threshold2 = params.get("threshold2", 200)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, threshold1, threshold2)
        return edges

class Cartoon(Style):
    name = "Cartoon"
    parameters = [
        {
            "name": "bilateral_filter_diameter",
            "type": "int",
            "default": 9,
            "min": 1,
            "max": 20,
            "step": 1,
            "label": "Bilateral Filter Diameter"
        },
        {
            "name": "bilateral_filter_sigmaColor",
            "type": "int",
            "default": 75,
            "min": 1,
            "max": 150,
            "step": 1,
            "label": "Bilateral Filter SigmaColor"
        },
        {
            "name": "bilateral_filter_sigmaSpace",
            "type": "int",
            "default": 75,
            "min": 1,
            "max": 150,
            "step": 1,
            "label": "Bilateral Filter SigmaSpace"
        },
        {
            "name": "canny_threshold1",
            "type": "int",
            "default": 100,
            "min": 0,
            "max": 500,
            "step": 1,
            "label": "Canny Threshold 1"
        },
        {
            "name": "canny_threshold2",
            "type": "int",
            "default": 200,
            "min": 0,
            "max": 500,
            "step": 1,
            "label": "Canny Threshold 2"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        d = params.get("bilateral_filter_diameter", 9)
        sigmaColor = params.get("bilateral_filter_sigmaColor", 75)
        sigmaSpace = params.get("bilateral_filter_sigmaSpace", 75)
        threshold1 = params.get("canny_threshold1", 100)
        threshold2 = params.get("canny_threshold2", 200)

        filtered = cv2.bilateralFilter(image, d, sigmaColor, sigmaSpace)
        gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, threshold1, threshold2)
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        cartoonized = cv2.bitwise_and(filtered, edges_colored)
        return cartoonized

class OilPainting(Style):
    name = "Oil Painting"
    parameters = [
        {
            "name": "radius",
            "type": "int",
            "default": 7,
            "min": 1,
            "max": 20,
            "step": 1,
            "label": "Radius"
        },
        {
            "name": "levels",
            "type": "int",
            "default": 8,
            "min": 1,
            "max": 20,
            "step": 1,
            "label": "Levels"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        radius = params.get("radius", 7)
        levels = params.get("levels", 8)
        oil_painted = cv2.xphoto.oilPainting(image, radius, levels)
        return oil_painted

class Mosaic(Style):
    name = "Mosaic"
    parameters = [
        {
            "name": "tile_size",
            "type": "int",
            "default": 10,
            "min": 2,
            "max": 50,
            "step": 1,
            "label": "Tile Size"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        tile_size = params.get("tile_size", 10)
        h, w = image.shape[:2]
        # Resize down and then up to create mosaic effect
        mosaic_image = cv2.resize(image, (w // tile_size, h // tile_size), interpolation=cv2.INTER_LINEAR)
        mosaic_image = cv2.resize(mosaic_image, (w, h), interpolation=cv2.INTER_NEAREST)
        return mosaic_image

class InvertColors(Style):
    name = "Invert Colors"
    parameters = [
        {
            "name": "invert_alpha",
            "type": "float",
            "default": 1.0,
            "min": 0.0,
            "max": 1.0,
            "step": 0.1,
            "label": "Invert Alpha"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        alpha = params.get("invert_alpha", 1.0)
        inverted = cv2.bitwise_not(image)
        # Blend original and inverted images based on alpha
        blended = cv2.addWeighted(image, 1 - alpha, inverted, alpha, 0)
        return blended

class Sharpen(Style):
    name = "Sharpen"
    parameters = [
        {
            "name": "kernel_size",
            "type": "int",
            "default": 3,
            "min": 1,
            "max": 5,
            "step": 2,
            "label": "Kernel Size"
        },
        {
            "name": "strength",
            "type": "float",
            "default": 1.0,
            "min": 0.5,
            "max": 3.0,
            "step": 0.1,
            "label": "Strength"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        kernel_size = params.get("kernel_size", 3)
        strength = params.get("strength", 1.0)
        kernel = np.array([[0, -1, 0],
                           [-1, 5 + strength, -1],
                           [0, -1, 0]])
        sharpened = cv2.filter2D(image, -1, kernel)
        return sharpened

class Emboss(Style):
    name = "Emboss"
    parameters = [
        {
            "name": "kernel_size",
            "type": "int",
            "default": 3,
            "min": 1,
            "max": 5,
            "step": 2,
            "label": "Kernel Size"
        },
        {
            "name": "scale",
            "type": "float",
            "default": 1.0,
            "min": 0.1,
            "max": 3.0,
            "step": 0.1,
            "label": "Scale"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        kernel_size = params.get("kernel_size", 3)
        scale = params.get("scale", 1.0)
        kernel = np.array([[-2, -1, 0],
                           [-1, 1, 1],
                           [0, 1, 2]])
        embossed = cv2.filter2D(image, -1, kernel) * scale + 128
        embossed = np.clip(embossed, 0, 255).astype(np.uint8)
        return embossed

class Vintage(Style):
    name = "Vintage"
    parameters = [
        {
            "name": "vintage_strength",
            "type": "float",
            "default": 0.5,
            "min": 0.0,
            "max": 1.0,
            "step": 0.1,
            "label": "Vintage Strength"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        strength = params.get("vintage_strength", 0.5)
        # Apply sepia
        sepia_filter = np.array([[0.272, 0.534, 0.131],
                                 [0.349, 0.686, 0.168],
                                 [0.393, 0.769, 0.189]])
        sepia = cv2.transform(image, sepia_filter)
        sepia = np.clip(sepia, 0, 255).astype(np.uint8)
        # Blend with original based on strength
        vintage = cv2.addWeighted(image, 1 - strength, sepia, strength, 0)
        return vintage

class Brightness(Style):
    name = "Brightness"
    parameters = [
        {
            "name": "brightness",
            "type": "int",
            "default": 0,
            "min": -100,
            "max": 100,
            "step": 5,
            "label": "Brightness"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        brightness = params.get("brightness", 0)
        brightened = cv2.convertScaleAbs(image, alpha=1, beta=brightness)
        return brightened

class Contrast(Style):
    name = "Contrast"
    parameters = [
        {
            "name": "contrast",
            "type": "float",
            "default": 1.0,
            "min": 0.5,
            "max": 3.0,
            "step": 0.1,
            "label": "Contrast"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        contrast = params.get("contrast", 1.0)
        contrasted = cv2.convertScaleAbs(image, alpha=contrast, beta=0)
        return contrasted

class HueSaturation(Style):
    name = "Hue & Saturation"
    parameters = [
        {
            "name": "hue",
            "type": "int",
            "default": 0,
            "min": -50,
            "max": 50,
            "step": 1,
            "label": "Hue"
        },
        {
            "name": "saturation",
            "type": "int",
            "default": 0,
            "min": -50,
            "max": 50,
            "step": 1,
            "label": "Saturation"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        hue = params.get("hue", 0)
        saturation = params.get("saturation", 0)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.int32)
        hsv[:, :, 0] = (hsv[:, :, 0] + hue) % 180
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] + saturation, 0, 255)
        hsv = hsv.astype(np.uint8)
        adjusted = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return adjusted

class Blur(Style):
    name = "Blur"
    parameters = [
        {
            "name": "kernel_size",
            "type": "int",
            "default": 5,
            "min": 1,
            "max": 31,
            "step": 2,
            "label": "Kernel Size"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        kernel_size = params.get("kernel_size", 5)
        if kernel_size % 2 == 0:
            kernel_size += 1
        blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        return blurred

class BrightnessContrast(Style):
    name = "Brightness & Contrast"
    parameters = [
        {
            "name": "brightness",
            "type": "int",
            "default": 0,
            "min": -100,
            "max": 100,
            "step": 5,
            "label": "Brightness"
        },
        {
            "name": "contrast",
            "type": "float",
            "default": 1.0,
            "min": 0.5,
            "max": 3.0,
            "step": 0.1,
            "label": "Contrast"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        brightness = params.get("brightness", 0)
        contrast = params.get("contrast", 1.0)
        adjusted = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
        return adjusted

class GammaCorrection(Style):
    name = "Gamma Correction"
    parameters = [
        {
            "name": "gamma",
            "type": "float",
            "default": 1.0,
            "min": 0.1,
            "max": 3.0,
            "step": 0.1,
            "label": "Gamma"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        gamma = params.get("gamma", 1.0)
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")
        corrected = cv2.LUT(image, table)
        return corrected

class Posterize(Style):
    name = "Posterize"
    parameters = [
        {
            "name": "bits",
            "type": "int",
            "default": 6,
            "min": 1,
            "max": 8,
            "step": 1,
            "label": "Bits"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        bits = params.get("bits", 6)
        shift = 8 - bits
        posterized = (image >> shift) << shift
        return posterized

class Solarize(Style):
    name = "Solarize"
    parameters = [
        {
            "name": "threshold",
            "type": "int",
            "default": 128,
            "min": 0,
            "max": 255,
            "step": 1,
            "label": "Threshold"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        threshold = params.get("threshold", 128)
        solarized = np.where(image < threshold, image, 255 - image)
        solarized = solarized.astype(np.uint8)
        return solarized

class Vibrance(Style):
    name = "Vibrance"
    parameters = [
        {
            "name": "vibrance",
            "type": "float",
            "default": 1.0,
            "min": 0.0,
            "max": 3.0,
            "step": 0.1,
            "label": "Vibrance"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        vibrance = params.get("vibrance", 1.0)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] *= vibrance
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
        hsv = hsv.astype(np.uint8)
        vibrant = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return vibrant

class Threshold(Style):
    name = "Threshold"
    parameters = [
        {
            "name": "threshold",
            "type": "int",
            "default": 128,
            "min": 0,
            "max": 255,
            "step": 1,
            "label": "Threshold"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        threshold = params.get("threshold", 128)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        return thresh

class BitwiseAnd(Style):
    name = "Bitwise AND"
    parameters = [
        {
            "name": "mask_intensity",
            "type": "int",
            "default": 128,
            "min": 0,
            "max": 255,
            "step": 1,
            "label": "Mask Intensity"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        intensity = params.get("mask_intensity", 128)
        mask = np.full(image.shape[:2], intensity, dtype=np.uint8)
        bitwise_and = cv2.bitwise_and(image, image, mask=mask)
        return bitwise_and

class BitwiseOr(Style):
    name = "Bitwise OR"
    parameters = [
        {
            "name": "mask_intensity",
            "type": "int",
            "default": 128,
            "min": 0,
            "max": 255,
            "step": 1,
            "label": "Mask Intensity"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        intensity = params.get("mask_intensity", 128)
        mask = np.full(image.shape[:2], intensity, dtype=np.uint8)
        bitwise_or = cv2.bitwise_or(image, image, mask=mask)
        return bitwise_or

class BitwiseXor(Style):
    name = "Bitwise XOR"
    parameters = [
        {
            "name": "mask_intensity",
            "type": "int",
            "default": 128,
            "min": 0,
            "max": 255,
            "step": 1,
            "label": "Mask Intensity"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        intensity = params.get("mask_intensity", 128)
        mask = np.full(image.shape[:2], intensity, dtype=np.uint8)
        bitwise_xor = cv2.bitwise_xor(image, image, mask=mask)
        return bitwise_xor

class GammaCorrection(Style):
    name = "Gamma Correction"
    parameters = [
        {
            "name": "gamma",
            "type": "float",
            "default": 1.0,
            "min": 0.1,
            "max": 3.0,
            "step": 0.1,
            "label": "Gamma"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        gamma = params.get("gamma", 1.0)
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")
        corrected = cv2.LUT(image, table)
        return corrected

class BrightnessContrast(Style):
    name = "Brightness & Contrast"
    parameters = [
        {
            "name": "brightness",
            "type": "int",
            "default": 0,
            "min": -100,
            "max": 100,
            "step": 5,
            "label": "Brightness"
        },
        {
            "name": "contrast",
            "type": "float",
            "default": 1.0,
            "min": 0.5,
            "max": 3.0,
            "step": 0.1,
            "label": "Contrast"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        brightness = params.get("brightness", 0)
        contrast = params.get("contrast", 1.0)
        adjusted = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
        return adjusted

class GammaCorrection(Style):
    name = "Gamma Correction"
    parameters = [
        {
            "name": "gamma",
            "type": "float",
            "default": 1.0,
            "min": 0.1,
            "max": 3.0,
            "step": 0.1,
            "label": "Gamma"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        gamma = params.get("gamma", 1.0)
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")
        corrected = cv2.LUT(image, table)
        return corrected

class Posterize(Style):
    name = "Posterize"
    parameters = [
        {
            "name": "bits",
            "type": "int",
            "default": 6,
            "min": 1,
            "max": 8,
            "step": 1,
            "label": "Bits"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        bits = params.get("bits", 6)
        shift = 8 - bits
        posterized = (image >> shift) << shift
        return posterized

class Solarize(Style):
    name = "Solarize"
    parameters = [
        {
            "name": "threshold",
            "type": "int",
            "default": 128,
            "min": 0,
            "max": 255,
            "step": 1,
            "label": "Threshold"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        threshold = params.get("threshold", 128)
        solarized = np.where(image < threshold, image, 255 - image)
        solarized = solarized.astype(np.uint8)
        return solarized

class Vibrance(Style):
    name = "Vibrance"
    parameters = [
        {
            "name": "vibrance",
            "type": "float",
            "default": 1.0,
            "min": 0.0,
            "max": 3.0,
            "step": 0.1,
            "label": "Vibrance"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        vibrance = params.get("vibrance", 1.0)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] *= vibrance
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
        hsv = hsv.astype(np.uint8)
        vibrant = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return vibrant

class Threshold(Style):
    name = "Threshold"
    parameters = [
        {
            "name": "threshold",
            "type": "int",
            "default": 128,
            "min": 0,
            "max": 255,
            "step": 1,
            "label": "Threshold"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        threshold = params.get("threshold", 128)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        return thresh

class BitwiseAnd(Style):
    name = "Bitwise AND"
    parameters = [
        {
            "name": "mask_intensity",
            "type": "int",
            "default": 128,
            "min": 0,
            "max": 255,
            "step": 1,
            "label": "Mask Intensity"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        intensity = params.get("mask_intensity", 128)
        mask = np.full(image.shape[:2], intensity, dtype=np.uint8)
        bitwise_and = cv2.bitwise_and(image, image, mask=mask)
        return bitwise_and

class BitwiseOr(Style):
    name = "Bitwise OR"
    parameters = [
        {
            "name": "mask_intensity",
            "type": "int",
            "default": 128,
            "min": 0,
            "max": 255,
            "step": 1,
            "label": "Mask Intensity"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        intensity = params.get("mask_intensity", 128)
        mask = np.full(image.shape[:2], intensity, dtype=np.uint8)
        bitwise_or = cv2.bitwise_or(image, image, mask=mask)
        return bitwise_or

class BitwiseXor(Style):
    name = "Bitwise XOR"
    parameters = [
        {
            "name": "mask_intensity",
            "type": "int",
            "default": 128,
            "min": 0,
            "max": 255,
            "step": 1,
            "label": "Mask Intensity"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        intensity = params.get("mask_intensity", 128)
        mask = np.full(image.shape[:2], intensity, dtype=np.uint8)
        bitwise_xor = cv2.bitwise_xor(image, image, mask=mask)
        return bitwise_xor

class HoughLines(Style):
    name = "Hough Lines"
    parameters = [
        {
            "name": "threshold",
            "type": "int",
            "default": 150,
            "min": 0,
            "max": 300,
            "step": 10,
            "label": "Threshold"
        },
        {
            "name": "minLineLength",
            "type": "int",
            "default": 100,
            "min": 50,
            "max": 300,
            "step": 10,
            "label": "Min Line Length"
        },
        {
            "name": "maxLineGap",
            "type": "int",
            "default": 10,
            "min": 0,
            "max": 100,
            "step": 5,
            "label": "Max Line Gap"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        threshold = params.get("threshold", 150)
        minLineLength = params.get("minLineLength", 100)
        maxLineGap = params.get("maxLineGap", 10)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold, minLineLength=minLineLength, maxLineGap=maxLineGap)
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return image

class CannyEdge(Style):
    name = "Canny Edge"
    parameters = [
        {
            "name": "threshold1",
            "type": "int",
            "default": 100,
            "min": 0,
            "max": 300,
            "step": 10,
            "label": "Threshold 1"
        },
        {
            "name": "threshold2",
            "type": "int",
            "default": 200,
            "min": 0,
            "max": 300,
            "step": 10,
            "label": "Threshold 2"
        },
        {
            "name": "apertureSize",
            "type": "int",
            "default": 3,
            "min": 3,
            "max": 7,
            "step": 2,
            "label": "Aperture Size"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        threshold1 = params.get("threshold1", 100)
        threshold2 = params.get("threshold2", 200)
        apertureSize = params.get("apertureSize", 3)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, threshold1, threshold2, apertureSize=apertureSize)
        return edges

class ColorBalance(Style):
    name = "Color Balance"
    parameters = [
        {
            "name": "blue_shift",
            "type": "int",
            "default": 0,
            "min": -50,
            "max": 50,
            "step": 1,
            "label": "Blue Shift"
        },
        {
            "name": "green_shift",
            "type": "int",
            "default": 0,
            "min": -50,
            "max": 50,
            "step": 1,
            "label": "Green Shift"
        },
        {
            "name": "red_shift",
            "type": "int",
            "default": 0,
            "min": -50,
            "max": 50,
            "step": 1,
            "label": "Red Shift"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        blue_shift = params.get("blue_shift", 0)
        green_shift = params.get("green_shift", 0)
        red_shift = params.get("red_shift", 0)
        # Split channels
        b, g, r = cv2.split(image)
        # Apply shifts
        b = cv2.add(b, blue_shift)
        g = cv2.add(g, green_shift)
        r = cv2.add(r, red_shift)
        # Merge back
        balanced = cv2.merge([b, g, r])
        return balanced

class BlurMotion(Style):
    name = "Motion Blur"
    parameters = [
        {
            "name": "kernel_size",
            "type": "int",
            "default": 15,
            "min": 3,
            "max": 51,
            "step": 2,
            "label": "Kernel Size"
        },
        {
            "name": "angle",
            "type": "int",
            "default": 0,
            "min": 0,
            "max": 360,
            "step": 10,
            "label": "Angle"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        kernel_size = params.get("kernel_size", 15)
        angle = params.get("angle", 0)
        if kernel_size % 2 == 0:
            kernel_size += 1
        # Create the motion blur kernel
        kernel = np.zeros((kernel_size, kernel_size))
        # Set the center row to ones
        kernel[int((kernel_size - 1)/2), :] = np.ones(kernel_size)
        # Rotate the kernel to the desired angle
        M = cv2.getRotationMatrix2D((kernel_size / 2 - 0.5, kernel_size / 2 - 0.5), angle, 1.0)
        rotated_kernel = cv2.warpAffine(kernel, M, (kernel_size, kernel_size))
        # Normalize the kernel
        rotated_kernel /= kernel_size
        # Apply the filter
        motion_blur = cv2.filter2D(image, -1, rotated_kernel)
        return motion_blur

class InvertFilter(Style):
    name = "Invert Filter"
    parameters = []

    def apply(self, image, params=None):
        inverted = cv2.bitwise_not(image)
        return inverted

class BrightnessOnly(Style):
    name = "Brightness Only"
    parameters = [
        {
            "name": "brightness",
            "type": "int",
            "default": 0,
            "min": -100,
            "max": 100,
            "step": 5,
            "label": "Brightness"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        brightness = params.get("brightness", 0)
        brightened = cv2.convertScaleAbs(image, alpha=1, beta=brightness)
        return brightened

class ContrastOnly(Style):
    name = "Contrast Only"
    parameters = [
        {
            "name": "contrast",
            "type": "float",
            "default": 1.0,
            "min": 0.5,
            "max": 3.0,
            "step": 0.1,
            "label": "Contrast"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        contrast = params.get("contrast", 1.0)
        contrasted = cv2.convertScaleAbs(image, alpha=contrast, beta=0)
        return contrasted

class Negative(Style):
    name = "Negative"
    parameters = []

    def apply(self, image, params=None):
        negative = cv2.bitwise_not(image)
        return negative

class SepiaVibrant(Style):
    name = "Sepia Vibrant"
    parameters = [
        {
            "name": "sepia_intensity",
            "type": "float",
            "default": 1.0,
            "min": 0.0,
            "max": 2.0,
            "step": 0.1,
            "label": "Sepia Intensity"
        },
        {
            "name": "vibrance",
            "type": "float",
            "default": 1.0,
            "min": 0.0,
            "max": 3.0,
            "step": 0.1,
            "label": "Vibrance"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        sepia_intensity = params.get("sepia_intensity", 1.0)
        vibrance = params.get("vibrance", 1.0)

        # Apply sepia
        sepia_filter = np.array([[0.272, 0.534, 0.131],
                                 [0.349, 0.686, 0.168],
                                 [0.393, 0.769, 0.189]])
        sepia = cv2.transform(image, sepia_filter)
        sepia = np.clip(sepia * sepia_intensity, 0, 255).astype(np.uint8)

        # Apply vibrance
        hsv = cv2.cvtColor(sepia, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] *= vibrance
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
        vibrant = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        return vibrant

class EmbossContrast(Style):
    name = "Emboss & Contrast"
    parameters = [
        {
            "name": "kernel_size",
            "type": "int",
            "default": 3,
            "min": 1,
            "max": 5,
            "step": 2,
            "label": "Kernel Size"
        },
        {
            "name": "scale",
            "type": "float",
            "default": 1.0,
            "min": 0.5,
            "max": 3.0,
            "step": 0.1,
            "label": "Scale"
        },
        {
            "name": "contrast",
            "type": "float",
            "default": 1.0,
            "min": 0.5,
            "max": 3.0,
            "step": 0.1,
            "label": "Contrast"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        kernel_size = params.get("kernel_size", 3)
        scale = params.get("scale", 1.0)
        contrast = params.get("contrast", 1.0)

        # Apply emboss
        kernel = np.array([[-2, -1, 0],
                           [-1, 1, 1],
                           [0, 1, 2]])
        embossed = cv2.filter2D(image, -1, kernel) * scale + 128
        embossed = np.clip(embossed, 0, 255).astype(np.uint8)

        # Apply contrast
        contrasted = cv2.convertScaleAbs(embossed, alpha=contrast, beta=0)
        return contrasted

class LightLeak(Style):
    name = "Light Leak"
    parameters = [
        {
            "name": "leak_intensity",
            "type": "int",
            "default": 50,
            "min": 0,
            "max": 100,
            "step": 5,
            "label": "Leak Intensity"
        },
        {
            "name": "leak_color",
            "type": "str",
            "default": "Red",
            "min": None,
            "max": None,
            "step": None,
            "label": "Leak Color",
            "options": ["Red", "Green", "Blue", "Yellow", "Cyan", "Magenta"]
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        intensity = params.get("leak_intensity", 50)
        color = params.get("leak_color", "Red").lower()

        overlay = image.copy()
        h, w = image.shape[:2]
        # Define color based on selection
        color_dict = {
            "red": (0, 0, 255),
            "green": (0, 255, 0),
            "blue": (255, 0, 0),
            "yellow": (0, 255, 255),
            "cyan": (255, 255, 0),
            "magenta": (255, 0, 255)
        }
        leak_color = color_dict.get(color, (0, 0, 255))

        # Draw a circle with increasing radius
        radius = int(min(h, w) * 0.3)
        cv2.circle(overlay, (w - radius, radius), radius, leak_color, -1)

        # Blend the overlay with the original image
        output = cv2.addWeighted(image, 1 - intensity / 100, overlay, intensity / 100, 0)
        return output

class Glitch(Style):
    name = "Glitch"
    parameters = [
        {
            "name": "max_shift",
            "type": "int",
            "default": 10,
            "min": 0,
            "max": 50,
            "step": 1,
            "label": "Max Shift"
        },
        {
            "name": "num_shifts",
            "type": "int",
            "default": 5,
            "min": 1,
            "max": 20,
            "step": 1,
            "label": "Number of Shifts"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        max_shift = params.get("max_shift", 10)
        num_shifts = params.get("num_shifts", 5)
        h, w = image.shape[:2]
        glitch = image.copy()
        for _ in range(num_shifts):
            # Randomly choose a channel
            channel = np.random.randint(0, 3)
            # Randomly choose a horizontal shift
            shift = np.random.randint(-max_shift, max_shift)
            # Apply the shift
            if shift > 0:
                glitch[:, :w - shift, channel] = image[:, shift:, channel]
                glitch[:, w - shift:, channel] = 0
            elif shift < 0:
                glitch[:, -shift:, channel] = image[:, :w + shift, channel]
                glitch[:, : -shift, channel] = 0
        return glitch

class VibrantColor(Style):
    name = "Vibrant Color"
    parameters = [
        {
            "name": "intensity",
            "type": "float",
            "default": 1.5,
            "min": 0.5,
            "max": 3.0,
            "step": 0.1,
            "label": "Intensity"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        intensity = params.get("intensity", 1.5)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] *= intensity  # Increase saturation
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
        vibrant = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        return vibrant

class NegativeVintage(Style):
    name = "Negative Vintage"
    parameters = [
        {
            "name": "sepia_intensity",
            "type": "float",
            "default": 1.0,
            "min": 0.0,
            "max": 2.0,
            "step": 0.1,
            "label": "Sepia Intensity"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        sepia_intensity = params.get("sepia_intensity", 1.0)
        # Invert colors
        inverted = cv2.bitwise_not(image)
        # Apply sepia
        sepia_filter = np.array([[0.272, 0.534, 0.131],
                                 [0.349, 0.686, 0.168],
                                 [0.393, 0.769, 0.189]])
        sepia = cv2.transform(inverted, sepia_filter)
        sepia = np.clip(sepia * sepia_intensity, 0, 255).astype(np.uint8)
        return sepia

class BlackWhite(Style):
    name = "Black & White"
    parameters = [
        {
            "name": "thresh",
            "type": "int",
            "default": 128,
            "min": 0,
            "max": 255,
            "step": 1,
            "label": "Threshold"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        thresh = params.get("thresh", 128)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        bw = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)[1]
        return bw

class ColorQuantization(Style):
    name = "Color Quantization"
    parameters = [
        {
            "name": "clusters",
            "type": "int",
            "default": 8,
            "min": 2,
            "max": 32,
            "step": 1,
            "label": "Clusters"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        clusters = params.get("clusters", 8)
        Z = image.reshape((-1,3))
        Z = np.float32(Z)
        # Define criteria and apply kmeans
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, centers = cv2.kmeans(Z, clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        centers = np.uint8(centers)
        res = centers[labels.flatten()]
        quantized = res.reshape((image.shape))
        return quantized

class Watercolor(Style):
    name = "Watercolor"
    parameters = [
        {
            "name": "sigma_s",
            "type": "int",
            "default": 60,
            "min": 10,
            "max": 100,
            "step": 10,
            "label": "Sigma S"
        },
        {
            "name": "sigma_r",
            "type": "float",
            "default": 0.5,
            "min": 0.1,
            "max": 1.0,
            "step": 0.1,
            "label": "Sigma R"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        sigma_s = params.get("sigma_s", 60)
        sigma_r = params.get("sigma_r", 0.5)
        watercolor = cv2.stylization(image, sigma_s=sigma_s, sigma_r=sigma_r)
        return watercolor

class Halftone(Style):
    name = "Halftone"
    parameters = [
        {
            "name": "dot_size",
            "type": "int",
            "default": 5,
            "min": 1,
            "max": 20,
            "step": 1,
            "label": "Dot Size"
        },
        {
            "name": "threshold",
            "type": "int",
            "default": 127,
            "min": 0,
            "max": 255,
            "step": 5,
            "label": "Threshold"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        dot_size = params.get("dot_size", 5)
        threshold = params.get("threshold", 127)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        halftone = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        for y in range(0, halftone.shape[0], dot_size*2):
            for x in range(0, halftone.shape[1], dot_size*2):
                if binary[y, x] == 0:
                    cv2.circle(halftone, (x, y), dot_size, (0,0,0), -1)
        return halftone

class GlowingEdges(Style):
    name = "Glowing Edges"
    parameters = [
        {
            "name": "edge_threshold",
            "type": "int",
            "default": 100,
            "min": 0,
            "max": 300,
            "step": 10,
            "label": "Edge Threshold"
        },
        {
            "name": "blur_size",
            "type": "int",
            "default": 7,
            "min": 1,
            "max": 21,
            "step": 2,
            "label": "Blur Size"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        edge_threshold = params.get("edge_threshold", 100)
        blur_size = params.get("blur_size", 7)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, edge_threshold, edge_threshold * 2)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        blurred = cv2.GaussianBlur(edges, (blur_size, blur_size), 0)
        glowing = cv2.addWeighted(image, 0.8, blurred, 0.2, 0)
        return glowing

# Add more styles here following the same pattern
