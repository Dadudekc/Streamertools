import pytest
import numpy as np
from styles.artistic.stippling import Stippling

@pytest.fixture
def dummy_image():
    return np.ones((100, 100, 3), dtype=np.uint8) * 255

def test_stippling_default(dummy_image):
    stippling = Stippling()
    result = stippling.apply(dummy_image, {})
    assert result.shape == dummy_image.shape[:2], "Output shape mismatch"
    assert result.dtype == np.uint8, "Output data type mismatch"

def test_stippling_custom_params(dummy_image):
    stippling = Stippling()
    params = {"dot_density": 5, "contrast_adjustment": 1.5}
    result = stippling.apply(dummy_image, params)
    assert result is not None, "Output is None"
    assert result.shape == dummy_image.shape[:2], "Output shape mismatch"
