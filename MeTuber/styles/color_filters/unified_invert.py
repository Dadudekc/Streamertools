# styles/color_filters/unified_invert.py
import cv2
import numpy as np
from typing import Any, Dict, Optional, List
from styles.base import Style


class InvertStyle(Style):
    """
    Unified Invert style that consolidates multiple invert/negative variants into a single class.
    Supports Colors, Filter, and Negative modes.
    """
    
    name = "Invert"
    category = "Color Filters"
    variants = ["Colors", "Filter", "Negative"]
    default_variant = "Colors"

    def __init__(self):
        super().__init__()

    def define_parameters(self) -> List[Dict[str, Any]]:
        """Define base parameters for invert effect."""
        return [
            {
                "name": "mode",
                "type": "str",
                "default": "Colors",
                "options": ["Colors", "Filter", "Negative"],
                "label": "Invert Mode"
            },
            {
                "name": "intensity",
                "type": "float",
                "default": 1.0,
                "min": 0.0,
                "max": 1.0,
                "step": 0.1,
                "label": "Invert Intensity"
            },
            {
                "name": "preserve_luminance",
                "type": "bool",
                "default": False,
                "label": "Preserve Luminance"
            }
        ]

    def define_variant_parameters(self, variant: str) -> List[Dict[str, Any]]:
        """Define variant-specific parameters."""
        if variant == "Filter":
            return [
                {
                    "name": "filter_strength",
                    "type": "float",
                    "default": 0.8,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.1,
                    "label": "Filter Strength"
                },
                {
                    "name": "apply_to_shadows",
                    "type": "bool",
                    "default": True,
                    "label": "Apply to Shadows"
                }
            ]
        elif variant == "Negative":
            return [
                {
                    "name": "negative_contrast",
                    "type": "float",
                    "default": 1.2,
                    "min": 0.5,
                    "max": 2.0,
                    "step": 0.1,
                    "label": "Negative Contrast"
                },
                {
                    "name": "preserve_highlights",
                    "type": "bool",
                    "default": False,
                    "label": "Preserve Highlights"
                }
            ]
        return []

    def apply(self, image: np.ndarray, params: Optional[Dict[str, Any]] = None) -> np.ndarray:
        """Apply invert effect based on selected variant."""
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Input image must be a valid NumPy array")

        # Validate and get parameters
        params = self.validate_params(params or {})
        variant = params.get("mode", self.current_variant)
        
        # Apply variant-specific processing
        if variant == "Colors":
            return self._apply_color_invert(image, params)
        elif variant == "Filter":
            return self._apply_filter_invert(image, params)
        elif variant == "Negative":
            return self._apply_negative_invert(image, params)
        else:
            raise ValueError(f"Unknown invert variant: {variant}")

    def _apply_color_invert(self, image: np.ndarray, params: Dict[str, Any]) -> np.ndarray:
        """Apply color inversion effect."""
        intensity = params.get("intensity", 1.0)
        preserve_luminance = params.get("preserve_luminance", False)
        
        if preserve_luminance:
            # Convert to HSV and invert only hue and saturation
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Invert hue (shift by 180 degrees)
            hsv[:, :, 0] = (hsv[:, :, 0] + 90) % 180
            
            # Invert saturation
            hsv[:, :, 1] = 255 - hsv[:, :, 1]
            
            # Keep value (luminance) unchanged
            result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        else:
            # Simple color inversion
            result = 255 - image
        
        # Apply intensity
        if intensity < 1.0:
            result = cv2.addWeighted(image, 1 - intensity, result, intensity, 0)
        
        return result

    def _apply_filter_invert(self, image: np.ndarray, params: Dict[str, Any]) -> np.ndarray:
        """Apply filter-based inversion effect."""
        intensity = params.get("intensity", 1.0)
        filter_strength = params.get("filter_strength", 0.8)
        apply_to_shadows = params.get("apply_to_shadows", True)
        
        # Convert to grayscale for luminance analysis
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Create mask based on luminance
        if apply_to_shadows:
            # Apply inversion to darker areas
            mask = gray < 128
        else:
            # Apply inversion to brighter areas
            mask = gray > 128
        
        # Create inverted version
        inverted = 255 - image
        
        # Apply filter effect
        filtered = cv2.addWeighted(image, 1 - filter_strength, inverted, filter_strength, 0)
        
        # Apply selective inversion
        result = image.copy()
        result[mask] = filtered[mask]
        
        # Apply overall intensity
        if intensity < 1.0:
            result = cv2.addWeighted(image, 1 - intensity, result, intensity, 0)
        
        return result

    def _apply_negative_invert(self, image: np.ndarray, params: Dict[str, Any]) -> np.ndarray:
        """Apply negative film effect."""
        intensity = params.get("intensity", 1.0)
        negative_contrast = params.get("negative_contrast", 1.2)
        preserve_highlights = params.get("preserve_highlights", False)
        
        # Create negative effect
        negative = 255 - image
        
        # Apply contrast adjustment
        negative = cv2.convertScaleAbs(negative, alpha=negative_contrast, beta=0)
        
        # Preserve highlights if enabled
        if preserve_highlights:
            # Create highlight mask
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            highlight_mask = gray > 200
            
            # Blend original highlights with negative
            result = negative.copy()
            result[highlight_mask] = image[highlight_mask]
        else:
            result = negative
        
        # Apply intensity
        if intensity < 1.0:
            result = cv2.addWeighted(image, 1 - intensity, result, intensity, 0)
        
        return result

    def _apply_selective_invert(self, image: np.ndarray, channel: int, intensity: float = 1.0) -> np.ndarray:
        """Apply inversion to a specific color channel."""
        result = image.copy()
        result[:, :, channel] = 255 - result[:, :, channel]
        
        if intensity < 1.0:
            result = cv2.addWeighted(image, 1 - intensity, result, intensity, 0)
        
        return result

    def _apply_hue_shift_invert(self, image: np.ndarray, shift_degrees: int = 180) -> np.ndarray:
        """Apply hue shift inversion."""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Shift hue by specified degrees
        hsv[:, :, 0] = (hsv[:, :, 0] + shift_degrees // 2) % 180
        
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR) 