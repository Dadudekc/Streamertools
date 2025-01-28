import pytest
import numpy as np
from MeTuber.styles.artistic.watercolor import Watercolor


@pytest.fixture
def dummy_image():
    """Creates a dummy 3-channel BGR image for testing."""
    return np.ones((100, 100, 3), dtype=np.uint8) * 255


def test_watercolor_default_params(dummy_image):
    """Tests the Watercolor style with default parameters."""
    watercolor = Watercolor()
    result = watercolor.apply(dummy_image)
    assert result is not None, "Watercolor effect returned None."
    assert result.shape == dummy_image.shape, "Output image shape mismatch."


def test_watercolor_custom_params(dummy_image):
    """Tests the Watercolor style with custom parameters."""
    watercolor = Watercolor()
    params = {"sigma_s": 80, "sigma_r": 0.7}
    result = watercolor.apply(dummy_image, params)
    assert result is not None, "Watercolor effect returned None with custom parameters."
    assert result.shape == dummy_image.shape, "Output image shape mismatch."


def test_watercolor_invalid_image():
    """Tests the Watercolor style with an invalid image."""
    watercolor = Watercolor()
    with pytest.raises(ValueError, match="Input image cannot be None."):
        watercolor.apply(None)


def test_watercolor_invalid_dtype():
    """Tests the Watercolor style with an invalid image dtype."""
    watercolor = Watercolor()
    invalid_image = np.array([[100, 150], [200, 250]])  # Grayscale image
    with pytest.raises(ValueError, match="Input image must be a 3-channel BGR image."):
        watercolor.apply(invalid_image)


def test_watercolor_invalid_params(dummy_image):
    """Tests the Watercolor style with out-of-range parameters."""
    watercolor = Watercolor()

    # Out-of-bounds test for sigma_s
    with pytest.raises(ValueError):
        watercolor.apply(dummy_image, {"sigma_s": 150, "sigma_r": 0.5})

    # Out-of-bounds test for sigma_r
    with pytest.raises(ValueError):
        watercolor.apply(dummy_image, {"sigma_s": 60, "sigma_r": 1.5})


def test_watercolor_no_params(dummy_image):
    """Tests the Watercolor style with no parameters provided."""
    watercolor = Watercolor()
    result = watercolor.apply(dummy_image)  # Should use default params
    assert result is not None, "Watercolor effect returned None with no parameters."
    assert result.shape == dummy_image.shape, "Output image shape mismatch."
