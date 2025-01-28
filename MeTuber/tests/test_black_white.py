import pytest
import numpy as np
from styles.effects.black_white import BlackWhite
import cv2

@pytest.fixture
def dummy_image():
    """Create a dummy image for testing."""
    return np.full((100, 100, 3), 128, dtype=np.uint8)

def test_black_white_default(dummy_image):
    black_white = BlackWhite()
    result = black_white.apply(dummy_image, {"threshold": 128})
    assert result is not None, "Result should not be None"
    assert result.shape == dummy_image.shape[:2], "Result shape mismatch"

def test_black_white_invalid_params(dummy_image):
    black_white = BlackWhite()
    with pytest.raises(ValueError):
        black_white.apply(dummy_image, {"threshold": -10})

def test_black_white_custom_threshold(dummy_image):
    black_white = BlackWhite()
    params = {"threshold": 100}
    result = black_white.apply(dummy_image, params)
    assert result is not None, "Result is None"
    assert result.shape == dummy_image.shape[:2], "Output shape mismatch"
