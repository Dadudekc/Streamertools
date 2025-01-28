import pytest
import numpy as np
from styles.basic.vibrant_color import VibrantColor


@pytest.fixture
def dummy_image():
    """Create a synthetic colorful image for testing."""
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    image[:, :, 0] = 100  # Blue channel
    image[:, :, 1] = 150  # Green channel
    image[:, :, 2] = 200  # Red channel
    return image

def test_vibrant_color_default_params(dummy_image):
    """
    Test VibrantColor with default parameters.
    """
    vibrant_color = VibrantColor()

    # Apply with default parameters
    result = vibrant_color.apply(dummy_image)
    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape
    # Ensure the image is modified
    assert not np.array_equal(result, dummy_image)


def test_vibrant_color_custom_params(dummy_image):
    """
    Test VibrantColor with custom parameters.
    """
    vibrant_color = VibrantColor()
    params = {"intensity": 2.0}

    # Apply with custom parameters
    result = vibrant_color.apply(dummy_image, params)
    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape
    # Ensure the image is modified differently than the default
    default_result = vibrant_color.apply(dummy_image)
    assert not np.array_equal(result, default_result)


def test_vibrant_color_zero_intensity(dummy_image):
    """
    Test VibrantColor with minimum intensity (no vibrancy effect).
    """
    vibrant_color = VibrantColor()
    params = {"intensity": 0.5}

    # Apply with zero intensity
    result = vibrant_color.apply(dummy_image, params)
    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape
    # Ensure the image is different because vibrance is very low
    assert not np.array_equal(result, dummy_image)


def test_vibrant_color_max_intensity(dummy_image):
    """
    Test VibrantColor with maximum intensity.
    """
    vibrant_color = VibrantColor()
    params = {"intensity": 3.0}

    # Apply with maximum intensity
    result = vibrant_color.apply(dummy_image, params)
    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape
    # Ensure the image is modified
    assert not np.array_equal(result, dummy_image)

def test_vibrant_color_invalid_image():
    """
    Test VibrantColor with invalid image input.
    """
    vibrant_color = VibrantColor()

    # Test with None as the image
    with pytest.raises(ValueError, match="Invalid image provided. Expected a NumPy array."):
        vibrant_color.apply(None)
