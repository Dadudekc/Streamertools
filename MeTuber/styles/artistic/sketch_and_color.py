import cv2
from styles.base import Style

class SketchAndColor(Style):
    """
    A style that combines a pencil sketch effect with color.
    """
    name = "Sketch & Color"
    category = "Artistic Styles"
    parameters = [
        {
            "name": "blur_intensity",
            "type": "int",
            "default": 21,
            "min": 1,
            "max": 51,
            "step": 2,
            "label": "Blur Intensity"
        },
        {
            "name": "color_strength",
            "type": "float",
            "default": 0.5,
            "min": 0.0,
            "max": 1.0,
            "step": 0.1,
            "label": "Color Strength"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        params = self.validate_params(params)

        blur_intensity = params["blur_intensity"]
        color_strength = params["color_strength"]

        # Ensure blur intensity is odd
        if blur_intensity % 2 == 0:
            blur_intensity += 1

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Invert grayscale
        inverted_gray = cv2.bitwise_not(gray)

        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(inverted_gray, (blur_intensity, blur_intensity), 0)

        # Invert blurred image
        inverted_blur = cv2.bitwise_not(blurred)

        # Create pencil sketch
        sketch = cv2.divide(gray, inverted_blur, scale=256.0)

        # Blend sketch with original image
        sketch_and_color = cv2.addWeighted(image, color_strength, cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR), 1 - color_strength, 0)

        return sketch_and_color
