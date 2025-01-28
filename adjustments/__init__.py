from .sharpen import Sharpen
from .emboss import Emboss
from .vintage import Vintage
from .hue_saturation import HueSaturation
from .blur import Blur
from .gamma_correction import GammaCorrection
from .posterize import Posterize
from .solarize import Solarize
from .vibrance import Vibrance
from .threshold import Threshold
from .brightness_contrast import BrightnessContrast

# List of all available adjustments
adjustments = [
    Sharpen,
    Emboss,
    Vintage,
    BrightnessContrast,
    HueSaturation,
    Blur,
    GammaCorrection,
    Posterize,
    Solarize,
    Vibrance,
    Threshold
]
