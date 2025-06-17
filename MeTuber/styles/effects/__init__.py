# styles/effects/__init__.py

from .emboss_contrast import EmbossContrast
from .black_white import BlackWhite
from .color_quantization import ColorQuantization
from .lines import HoughLines, CannyEdge
from ..artistic.watercolor import Watercolor

__all__ = [
    "EmbossContrast",
    "BlackWhite",
    "ColorQuantization",
    "HoughLines",
    "CannyEdge",
    "Watercolor",
]
