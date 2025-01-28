import pytest
import numpy as np
from styles.artistic.line_art import LineArt

@pytest.fixture
def dummy_image():
    return np.ones((100, 100, 3), dtype=np.uint8) * 255

def test_line_art_default(dummy_image):
    line_art = LineArt()
    result = line_art.apply(dummy_image, {})
    assert result.shape == dummy_image.shape[:2], "Output shape mismatch"
    assert result.dtype == np.uint8, "Output data type mismatch"

def test_line_art_custom_threshold(dummy_image):
    line_art = LineArt()
    params = {"threshold1": 30, "threshold2": 100}
    result = line_art.apply(dummy_image, params)
    assert result is not None, "Output is None"
    assert result.shape == dummy_image.shape[:2], "Output shape mismatch"
