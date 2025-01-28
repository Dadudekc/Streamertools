import pytest
import numpy as np
from styles.effects.misc.watercolor import Watercolor


@pytest.fixture
def dummy_image():
    """
    Creates a dummy image for testing.
    """
    return np.ones((100, 100, 3), dtype=np.uint8) * 255


def test_watercolor_default_params(dummy_image):
    """
    Tests the Watercolor style with default parameters.
    """
    watercolor = Watercolor()
    result = watercolor.apply(dummy_image)
    assert result is not None, "Watercolor effect returned None."
    assert result.shape == dummy_image.shape, "Output image shape mismatch."


def test_watercolor_custom_params(dummy_image):
    """
    Tests the Watercolor style with custom parameters.
    """
    watercolor = Watercolor()
    params = {"sigma_s": 80, "sigma_r": 0.7}
    result = watercolor.apply(dummy_image, params)
    assert result is not None, "Watercolor effect returned None with custom parameters."
    assert result.shape == dummy_image.shape, "Output image shape mismatch."


def test_watercolor_invalid_image():
    """
    Tests the Watercolor style with an invalid image.
    """
    watercolor = Watercolor()
    with pytest.raises(ValueError, match="Input image must be a valid NumPy array."):
        watercolor.apply(None)


def test_watercolor_invalid_params(dummy_image):
    """
    Tests the Watercolor style with invalid parameters.
    """
    watercolor = Watercolor()

    # Out of bounds parameter test
    with pytest.raises(ValueError):
        watercolor.apply(dummy_image, {"sigma_s": 150, "sigma_r": 1.5})
