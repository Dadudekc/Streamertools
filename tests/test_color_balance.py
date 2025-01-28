import pytest
import cv2
import numpy as np
from styles.basic.color_balance import ColorBalance


@pytest.fixture
def dummy_image():
    """Create a dummy image for testing."""
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    image[:, :, 0] = 100  # Blue channel
    image[:, :, 1] = 150  # Green channel
    image[:, :, 2] = 200  # Red channel
    return image


def test_color_balance_default_params(dummy_image):
    """Test ColorBalance with default parameters."""
    color_balance = ColorBalance()
    result = color_balance.apply(dummy_image)
    assert result is not None, "Result should not be None."
    assert result.shape == dummy_image.shape, "Output dimensions should match input."
    assert np.array_equal(result, dummy_image), "Default parameters should not alter the image."


def test_color_balance_increase_blue(dummy_image):
    """Test ColorBalance with increased blue channel."""
    color_balance = ColorBalance()
    params = {"blue_shift": 30}
    result = color_balance.apply(dummy_image, params)
    assert result is not None, "Result should not be None."
    assert result.shape == dummy_image.shape, "Output dimensions should match input."
    assert (result[:, :, 0] > dummy_image[:, :, 0]).all(), "Blue channel should increase."


def test_color_balance_decrease_green(dummy_image):
    """Test ColorBalance with decreased green channel."""
    color_balance = ColorBalance()
    params = {"green_shift": -30}
    result = color_balance.apply(dummy_image, params)
    assert result is not None, "Result should not be None."
    assert result.shape == dummy_image.shape, "Output dimensions should match input."
    assert (result[:, :, 1] < dummy_image[:, :, 1]).all(), "Green channel should decrease."


def test_color_balance_adjust_all_channels(dummy_image):
    """Test ColorBalance by adjusting all color channels."""
    color_balance = ColorBalance()
    params = {"blue_shift": 20, "green_shift": -20, "red_shift": 10}
    result = color_balance.apply(dummy_image, params)
    assert result is not None, "Result should not be None."
    assert result.shape == dummy_image.shape, "Output dimensions should match input."
    assert (result[:, :, 0] > dummy_image[:, :, 0]).all(), "Blue channel should increase."
    assert (result[:, :, 1] < dummy_image[:, :, 1]).all(), "Green channel should decrease."
    assert (result[:, :, 2] > dummy_image[:, :, 2]).all(), "Red channel should increase."


def test_color_balance_invalid_image():
    """Test ColorBalance with an invalid image."""
    color_balance = ColorBalance()
    with pytest.raises(ValueError, match="Input image cannot be None."):
        color_balance.apply(None)


def test_color_balance_out_of_range_params(dummy_image):
    """Test ColorBalance with out-of-range parameters."""
    color_balance = ColorBalance()

    # Test below the minimum value
    with pytest.raises(ValueError, match="Parameter 'blue_shift' must be between -50 and 50."):
        color_balance.apply(dummy_image, {"blue_shift": -100})

    # Test above the maximum value
    with pytest.raises(ValueError, match="Parameter 'red_shift' must be between -50 and 50."):
        color_balance.apply(dummy_image, {"red_shift": 100})
