# misc.py

import cv2
import numpy as np
from ..styles.base import Style

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
        params = self.validate_params(params)

        brightness = params["brightness"]
        return cv2.convertScaleAbs(image, alpha=1, beta=brightness)


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
        params = self.validate_params(params)

        contrast = params["contrast"]
        return cv2.convertScaleAbs(image, alpha=contrast, beta=0)


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
        params = self.validate_params(params)

        sepia_intensity = params["sepia_intensity"]
        vibrance = params["vibrance"]

        sepia_filter = np.array([[0.272, 0.534, 0.131],
                                 [0.349, 0.686, 0.168],
                                 [0.393, 0.769, 0.189]])
        sepia = cv2.transform(image, sepia_filter)
        sepia = np.clip(sepia * sepia_intensity, 0, 255).astype(np.uint8)

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
        params = self.validate_params(params)

        kernel_size = params["kernel_size"]
        scale = params["scale"]
        contrast = params["contrast"]

        kernel = np.array([[-2, -1, 0],
                           [-1,  1, 1],
                           [0,   1, 2]])
        embossed = cv2.filter2D(image, -1, kernel) * scale + 128
        embossed = np.clip(embossed, 0, 255).astype(np.uint8)

        contrasted = cv2.convertScaleAbs(embossed, alpha=contrast, beta=0)
        return contrasted


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
        params = self.validate_params(params)

        thresh = params["thresh"]
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
        params = self.validate_params(params)

        clusters = params["clusters"]
        Z = image.reshape((-1, 3)).astype(np.float32)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, centers = cv2.kmeans(Z, clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        centers = np.uint8(centers)
        res = centers[labels.flatten()]
        quantized = res.reshape(image.shape)
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
        params = self.validate_params(params)

        sigma_s = params["sigma_s"]
        sigma_r = params["sigma_r"]
        watercolor = cv2.stylization(image, sigma_s=sigma_s, sigma_r=sigma_r)
        return watercolor
