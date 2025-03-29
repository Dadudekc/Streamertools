# MeTuber\tests\test_vibrant_color.py

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
    """Test VibrantColor with default parameters."""
    vibrant_color = VibrantColor()
    result = vibrant_color.apply(dummy_image)
    assert isinstance(result, np.ndarray), "Result should be a NumPy array."
    assert result.shape == dummy_image.shape, "Output shape should match input."
    assert not np.array_equal(result, dummy_image), "Result should differ from input."


def test_vibrant_color_custom_params(dummy_image):
    """Test VibrantColor with custom parameters."""
    vibrant_color = VibrantColor()
    params = {"intensity": 2.0}
    result = vibrant_color.apply(dummy_image, params)
    assert isinstance(result, np.ndarray), "Result should be a NumPy array."
    assert result.shape == dummy_image.shape, "Output shape should match input."
    default_result = vibrant_color.apply(dummy_image)
    assert not np.array_equal(result, default_result), "Custom intensity should alter the image."


def test_vibrant_color_zero_intensity(dummy_image):
    """Test VibrantColor with minimum intensity (no vibrancy effect)."""
    vibrant_color = VibrantColor()
    params = {"intensity": 0.5}
    result = vibrant_color.apply(dummy_image, params)
    assert isinstance(result, np.ndarray), "Result should be a NumPy array."
    assert result.shape == dummy_image.shape, "Output shape should match input."
    # With lower intensity, colors should be less vibrant but still different from input
    assert not np.array_equal(result, dummy_image), "Low intensity should alter the image."


def test_vibrant_color_max_intensity(dummy_image):
    """Test VibrantColor with maximum intensity."""
    vibrant_color = VibrantColor()
    params = {"intensity": 3.0}
    result = vibrant_color.apply(dummy_image, params)
    assert isinstance(result, np.ndarray), "Result should be a NumPy array."
    assert result.shape == dummy_image.shape, "Output shape should match input."
    assert not np.array_equal(result, dummy_image), "High intensity should alter the image."


def test_vibrant_color_invalid_image():
    """Test VibrantColor with invalid image input."""
    vibrant_color = VibrantColor()

    invalid_inputs = [None, [], "not_an_image"]
    
    for invalid_input in invalid_inputs:
        with pytest.raises(ValueError) as exc_info:
            vibrant_color.apply(invalid_input)

        actual_message = str(exc_info.value)
        print(f"Captured error message: {actual_message}")  # Debugging output

        assert "Input image cannot be None" in actual_message or "Invalid image" in actual_message, \
            "Unexpected error message format."

def test_vibrant_color_edge_case_image():
    """Test VibrantColor with edge case images (e.g., grayscale, single pixel)."""
    vibrant_color = VibrantColor()

    # Test with a grayscale image
    grayscale_image = np.zeros((100, 100), dtype=np.uint8)
    
    # Now, grayscale should be converted to BGR instead of raising an error
    result = vibrant_color.apply(grayscale_image)
    assert isinstance(result, np.ndarray), "Result should be a NumPy array."
    assert result.shape == (100, 100, 3), "Grayscale should be converted to a 3-channel image."

    # Test with a single-pixel image
    single_pixel_image = np.array([[[100, 150, 200]]], dtype=np.uint8)
    result = vibrant_color.apply(single_pixel_image)
    assert isinstance(result, np.ndarray), "Result should be a NumPy array."
    assert result.shape == single_pixel_image.shape, "Output shape should match input."
