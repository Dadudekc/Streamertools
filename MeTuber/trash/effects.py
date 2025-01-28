# effects.py

import cv2
import numpy as np
from .base import Style

class ColorBalance(Style):
    name = "Color Balance"
    category = "Effects"
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
        params = self.validate_params(params)

        blue_shift = params["blue_shift"]
        green_shift = params["green_shift"]
        red_shift = params["red_shift"]

        b, g, r = cv2.split(image)
        b = cv2.add(b, blue_shift)
        g = cv2.add(g, green_shift)
        r = cv2.add(r, red_shift)

        balanced = cv2.merge([b, g, r])
        return balanced


class BlurMotion(Style):
    name = "Motion Blur"
    category = "Effects"
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
        params = self.validate_params(params)

        kernel_size = params["kernel_size"]
        angle = params["angle"]
        if kernel_size % 2 == 0:
            kernel_size += 1

        kernel = np.zeros((kernel_size, kernel_size))
        kernel[kernel_size // 2, :] = np.ones(kernel_size)
        M = cv2.getRotationMatrix2D((kernel_size / 2 - 0.5, kernel_size / 2 - 0.5), angle, 1.0)
        rotated_kernel = cv2.warpAffine(kernel, M, (kernel_size, kernel_size))
        rotated_kernel /= kernel_size
        motion_blur = cv2.filter2D(image, -1, rotated_kernel)
        return motion_blur


class LightLeak(Style):
    name = "Light Leak"
    category = "Effects"
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
            "label": "Leak Color",
            "options": ["Red", "Green", "Blue", "Yellow", "Cyan", "Magenta"]
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        params = self.validate_params(params)

        intensity = params["leak_intensity"]
        color = params["leak_color"].lower()

        overlay = image.copy()
        h, w = image.shape[:2]
        color_dict = {
            "red": (0, 0, 255),
            "green": (0, 255, 0),
            "blue": (255, 0, 0),
            "yellow": (0, 255, 255),
            "cyan": (255, 255, 0),
            "magenta": (255, 0, 255)
        }
        leak_color = color_dict.get(color, (0, 0, 255))

        radius = int(min(h, w) * 0.3)
        cv2.circle(overlay, (w - radius, radius), radius, leak_color, -1)

        output = cv2.addWeighted(image, 1 - intensity / 100, overlay, intensity / 100, 0)
        return output


class Glitch(Style):
    name = "Glitch"
    category = "Effects"
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
        params = self.validate_params(params)

        max_shift = params["max_shift"]
        num_shifts = params["num_shifts"]
        h, w = image.shape[:2]
        glitch = image.copy()

        for _ in range(num_shifts):
            channel = np.random.randint(0, 3)
            shift = np.random.randint(-max_shift, max_shift)
            if shift > 0:
                glitch[:, :w - shift, channel] = image[:, shift:, channel]
                glitch[:, w - shift:, channel] = 0
            elif shift < 0:
                glitch[:, -shift:, channel] = image[:, :w + shift, channel]
                glitch[:, :-shift, channel] = 0

        return glitch


class VibrantColor(Style):
    name = "Vibrant Color"
    category = "Effects"
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
        params = self.validate_params(params)

        intensity = params["intensity"]
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] *= intensity
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
        vibrant = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        return vibrant


class NegativeVintage(Style):
    name = "Negative Vintage"
    category = "Effects"
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
        params = self.validate_params(params)

        sepia_intensity = params["sepia_intensity"]
        inverted = cv2.bitwise_not(image)

        sepia_filter = np.array([[0.272, 0.534, 0.131],
                                 [0.349, 0.686, 0.168],
                                 [0.393, 0.769, 0.189]])
        sepia = cv2.transform(inverted, sepia_filter)
        sepia = np.clip(sepia * sepia_intensity, 0, 255).astype(np.uint8)
        return sepia


class Halftone(Style):
    name = "Halftone"
    category = "Effects"
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
        params = self.validate_params(params)

        dot_size = params["dot_size"]
        threshold = params["threshold"]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

        halftone = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        for y in range(0, halftone.shape[0], dot_size * 2):
            for x in range(0, halftone.shape[1], dot_size * 2):
                if binary[y, x] == 0:
                    cv2.circle(halftone, (x, y), dot_size, (0, 0, 0), -1)
        return halftone


class GlowingEdges(Style):
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
        params = self.validate_params(params)

        edge_threshold = params["edge_threshold"]
        blur_size = params["blur_size"]

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, edge_threshold, edge_threshold * 2)
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        blurred = cv2.GaussianBlur(edges_bgr, (blur_size, blur_size), 0)
        glowing = cv2.addWeighted(image, 0.8, blurred, 0.2, 0)
        return glowing
