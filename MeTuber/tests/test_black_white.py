import pytest
import numpy as np
from styles.effects.black_white import BlackWhite
import cv2

@pytest.fixture
def dummy_image():
    """Create a dummy image for testing."""
    return np.full((100, 100, 3), 128, dtype=np.uint8)

def test_black_white_default(dummy_image):
    """
    Test the Black & White effect with default parameters.
    """
    black_white = BlackWhite()
    result = black_white.apply(dummy_image)
    assert result is not None, "Result should not be None"
    assert result.shape == dummy_image.shape[:2], "Result shape mismatch"
    assert np.all((result == 0) | (result == 255)), "Output must be binary"

# Inside test_black_white.py
def test_black_white_invalid_params(dummy_image):
    black_white = BlackWhite()
    with pytest.raises(ValueError, match="Parameter 'threshold' must be between 0 and 255."):
        black_white.apply(dummy_image, {"threshold": -10})


def test_black_white_custom_threshold(dummy_image):
    """
    Test the Black & White effect with a custom threshold.
    """
    black_white = BlackWhite()
    params = {"threshold": 100}
    result = black_white.apply(dummy_image, params)
    assert result is not None, "Result is None"
    assert result.shape == dummy_image.shape[:2], "Output shape mismatch"
    assert np.all((result == 0) | (result == 255)), "Output must be binary"

def test_black_white_performance(dummy_image):
    black_white = BlackWhite()
    # Simulate applying the filter on multiple frames (e.g., 30 frames per second)
    for _ in range(30):
        result = black_white.apply(dummy_image)
        assert result is not None, "Result should not be None"
