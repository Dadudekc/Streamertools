import pytest
import cv2
import numpy as np
from styles.basic.brightness_only import BrightnessOnly


@pytest.fixture
def dummy_image():
    """Create a dummy image for testing."""
    image = np.ones((100, 100, 3), dtype=np.uint8) * 128
    return image


def test_brightness_only_default_params(dummy_image):
    """Test BrightnessOnly with default parameters."""
    brightness_only = BrightnessOnly()
    result = brightness_only.apply(dummy_image)
    assert result is not None, "Result should not be None."
    assert result.shape == dummy_image.shape, "Output dimensions should match input."
    assert np.array_equal(result, dummy_image), "Default parameters should not alter the image."


def test_brightness_only_increase_brightness(dummy_image):
    """Test BrightnessOnly with increased brightness."""
    brightness_only = BrightnessOnly()
    params = {"brightness": 50}
    result = brightness_only.apply(dummy_image, params)
    assert result is not None, "Result should not be None."
    assert result.shape == dummy_image.shape, "Output dimensions should match input."
    assert (result > dummy_image).all(), "All pixels should be brighter."


def test_brightness_only_decrease_brightness(dummy_image):
    """Test BrightnessOnly with decreased brightness."""
    brightness_only = BrightnessOnly()
    params = {"brightness": -50}
    result = brightness_only.apply(dummy_image, params)
    assert result is not None, "Result should not be None."
    assert result.shape == dummy_image.shape, "Output dimensions should match input."
    assert (result < dummy_image).all(), "All pixels should be darker."


def test_brightness_only_invalid_image():
    """Test BrightnessOnly with an invalid image."""
    brightness_only = BrightnessOnly()
    with pytest.raises(ValueError, match="Input image cannot be None."):
        brightness_only.apply(None)


def test_brightness_only_out_of_range_params(dummy_image):
    """Test BrightnessOnly with out-of-range parameters."""
    brightness_only = BrightnessOnly()

    # Test below the minimum value
    with pytest.raises(ValueError, match="Parameter 'brightness' must be between -100 and 100."):
        brightness_only.apply(dummy_image, {"brightness": -150})

    # Test above the maximum value
    with pytest.raises(ValueError, match="Parameter 'brightness' must be between -100 and 100."):
        brightness_only.apply(dummy_image, {"brightness": 150})
