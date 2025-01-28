import pytest
import numpy as np
import cv2
from styles.artistic.cartoon import Cartoon

@pytest.fixture
def dummy_image():
    """
    Create a dummy image for testing purposes.
    """
    dummy_image = np.ones((100, 100, 3), dtype=np.uint8) * 255
    return cv2.rectangle(dummy_image, (25, 25), (75, 75), (0, 255, 0), -1)

def test_cartoon_default_params(dummy_image):
    """
    Test the Cartoon effect with default parameters.
    """
    cartoon = Cartoon()
    result = cartoon.apply(dummy_image, {})
    assert result is not None, "The cartoon effect returned None."
    assert result.shape == dummy_image.shape, "Output shape mismatch."
    assert np.mean(result) < np.mean(dummy_image), "The cartoon effect did not alter the image as expected."

def test_cartoon_custom_params(dummy_image):
    """
    Test the Cartoon effect with custom parameters.
    """
    cartoon = Cartoon()
    params = {
        "bilateral_filter_diameter": 15,
        "bilateral_filter_sigmaColor": 125,
        "bilateral_filter_sigmaSpace": 125,
        "canny_threshold1": 30,
        "canny_threshold2": 100
    }
    result = cartoon.apply(dummy_image, params)
    assert result is not None, "The cartoon effect returned None with custom parameters."
    assert result.shape == dummy_image.shape, "Output shape mismatch with custom parameters."

def test_cartoon_invalid_params(dummy_image):
    """
    Test the Cartoon effect with invalid parameters.
    """
    cartoon = Cartoon()
    with pytest.raises(ValueError, match="Parameter 'bilateral_filter_diameter' must be between 1 and 20."):
        cartoon.apply(dummy_image, {"bilateral_filter_diameter": 25})
    with pytest.raises(ValueError, match="Parameter 'canny_threshold1' must be between 0 and 500."):
        cartoon.apply(dummy_image, {"canny_threshold1": -10})
    with pytest.raises(ValueError, match="Parameter 'bilateral_filter_sigmaColor' must be between 1 and 150."):
        cartoon.apply(dummy_image, {"bilateral_filter_sigmaColor": 200})
