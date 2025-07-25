import cv2
import numpy as np
from styles.base import Style

class BufferTestStyle(Style):
    name = "Buffer Test (Fast)"
    category = "Effects"
    parameters = [
        {
            "name": "brightness",
            "label": "Brightness",
            "type": "int",
            "default": 0,
            "min": -100,
            "max": 100
        },
        {
            "name": "contrast",
            "label": "Contrast",
            "type": "int",
            "default": 0,
            "min": -100,
            "max": 100
        }
    ]

    def apply(self, image, params):
        """Apply a very fast brightness/contrast adjustment to test buffer management."""
        brightness = params.get("brightness", 0)
        contrast = params.get("contrast", 0)
        
        # Fast brightness/contrast adjustment
        if brightness != 0 or contrast != 0:
            # Convert to float for calculations
            img_float = image.astype(np.float32)
            
            # Apply brightness
            if brightness != 0:
                img_float += brightness
            
            # Apply contrast
            if contrast != 0:
                factor = (259 * (contrast + 255)) / (255 * (259 - contrast))
                img_float = factor * (img_float - 128) + 128
            
            # Clip values and convert back to uint8
            image = np.clip(img_float, 0, 255).astype(np.uint8)
        
        return image 