import pytest
import numpy as np
from styles.artistic.sketch_and_color import SketchAndColor

@pytest.fixture
def dummy_image():
    return np.ones((100, 100, 3), dtype=np.uint8) * 255

def test_sketch_and_color_default(dummy_image):
    sketch_and_color = SketchAndColor()
    result = sketch_and_color.apply(dummy_image, {})
    assert result.shape == dummy_image.shape, "Output shape mismatch"
    assert result.dtype == np.uint8, "Output data type mismatch"

def test_sketch_and_color_custom(dummy_image):
    sketch_and_color = SketchAndColor()
    params = {"blur_intensity": 15, "color_strength": 0.8}
    result = sketch_and_color.apply(dummy_image, params)
    assert result is not None, "Output is None"
    assert result.shape == dummy_image.shape, "Output shape mismatch"
