import pytest
import numpy as np
from styles.distortions.halftone import Halftone

@pytest.fixture
def dummy_image():
    return np.full((100, 100, 3), 128, dtype=np.uint8)  # A gray image

def test_halftone_default_params(dummy_image):
    """
    Test Halftone effect with default parameters.
    """
    halftone = Halftone()
    result = halftone.apply(dummy_image)

    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape
    assert np.any(result != dummy_image)  # Ensure the effect modifies the image

def test_halftone_custom_params(dummy_image):
    """
    Test Halftone effect with custom dot size and threshold.
    """
    halftone = Halftone()
    params = {"dot_size": 3, "threshold": 100}
    result = halftone.apply(dummy_image, params)

    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape

def test_halftone_invalid_image():
    """
    Test Halftone effect with invalid image input.
    """
    halftone = Halftone()
    with pytest.raises(ValueError, match="Invalid image provided. Expected a NumPy array."):
        halftone.apply(None)

def test_halftone_boundary_threshold(dummy_image):
    """
    Test Halftone effect with extreme threshold values.
    """
    halftone = Halftone()

    # Threshold = 0 (everything should be black)
    params_low = {"threshold": 0, "dot_size": 3}
    result_low = halftone.apply(dummy_image, params_low)
    assert np.all(result_low == 0)  # Ensure all pixels are black

    # Threshold = 255 (everything should be white)
    params_high = {"threshold": 255, "dot_size": 3}
    result_high = halftone.apply(dummy_image, params_high)
    assert np.all(result_high == 255)  # Ensure all pixels are white
