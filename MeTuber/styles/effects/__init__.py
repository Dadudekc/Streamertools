# styles/effects/misc/__init__.py

from ..basic.brightness_only import BrightnessOnly
from ..basic.contrast_only import ContrastOnly
from ..basic.sepia_vibrant import SepiaVibrant
from .emboss_contrast import EmbossContrast
from .black_white import BlackWhite
from .color_quantization import ColorQuantization
from MeTuber.styles.artistic.watercolor import Watercolor
from MeTuber.styles.effects.lines import HoughLines, CannyEdge
# Import other effects as needed

__all__ = [
    "BrightnessOnly",
    "ContrastOnly",
    "SepiaVibrant",
    "EmbossContrast",
    "BlackWhite",
    "ColorQuantization",
    "Watercolor",
]
