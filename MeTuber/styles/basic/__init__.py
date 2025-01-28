# styles/basic/__init__.py

from ..basic.brightness_only import BrightnessOnly
from ..basic.contrast_only import ContrastOnly
from ..basic.sepia_vibrant import SepiaVibrant

from .brightness_only import BrightnessOnly
from .contrast_only import ContrastOnly
from .color_balance import ColorBalance


__all__ = [
    "BrightnessOnly",
    "ContrastOnly",
    "SepiaVibrant",
    "EmbossContrast",
    "BlackWhite",
    "ColorQuantization",
    "Watercolor",
]
