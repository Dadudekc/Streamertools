import cv2
import numpy as np
import pytest
from styles.adjustments.solarize import Solarize


@pytest.fixture
def dummy_image():
    """Generate a dummy grayscale image for testing."""
    return np.array([[100, 150], [200, 250]], dtype=np.uint8)


def test_solarize_default_threshold(dummy_image):
    """Test solarize with the default threshold."""
    solarize = Solarize()
    params = {"threshold": 128}
    result = solarize.apply(dummy_image, params)
    expected = np.array([[100, 105], [55, 5]], dtype=np.uint8)  # Correct expected values
    assert np.array_equal(result, expected), f"Expected {expected}, got {result}"


def test_solarize_custom_threshold():
    """Test solarize with a custom threshold."""
    solarize = Solarize()
    input_image = np.array([[100, 150], [200, 50]], dtype=np.uint8)
    params = {"threshold": 150}
    expected = np.array([[100, 105], [55, 50]], dtype=np.uint8)  # Updated expected values
    result = solarize.apply(input_image, params)
    assert np.array_equal(result, expected), f"Got {result}, expected {expected}"


def test_solarize_invalid_image_type():
    """Test solarize with an invalid image type."""
    solarize = Solarize()
    invalid_image = "not_an_image"
    with pytest.raises(ValueError, match="Input must be a valid NumPy array."):
        solarize.apply(invalid_image, {"threshold": 128})


def test_solarize_invalid_dtype():
    """Test solarize with an invalid image dtype."""
    solarize = Solarize()
    invalid_image = np.array([[100.0, 150.0], [200.0, 250.0]])  # Float array
    with pytest.raises(ValueError, match="Input image must have dtype of np.uint8."):
        solarize.apply(invalid_image, {"threshold": 128})


def test_solarize_no_params(dummy_image):
    """Test solarize with no parameters provided."""
    solarize = Solarize()
    result = solarize.apply(dummy_image)  # Should use default params
    expected = np.array([[100, 105], [55, 5]], dtype=np.uint8)
    assert np.array_equal(result, expected), f"Expected {expected}, got {result}"
