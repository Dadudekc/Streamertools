# D:\MeTuber\test_template.py

import pytest
import cv2
import numpy as np
from styles.effects.<MODULE_NAME> import <CLASS_NAME>

@pytest.fixture
def dummy_image():
    # Create a simple dummy image for testing
    return np.ones((100, 100, 3), dtype=np.uint8) * 255

def test_<STYLE_NAME>_default(dummy_image):
    style = <CLASS_NAME>()
    result = style.apply(dummy_image, {})
    assert result.shape == dummy_image.shape, "Output shape mismatch"
    assert result is not None, "Resulting image is None"

def test_<STYLE_NAME>_custom_params(dummy_image):
    style = <CLASS_NAME>()
    params = {<"param_name">: <value>, ...}
    result = style.apply(dummy_image, params)
    assert result is not None, "Resulting image is None"
    assert result.shape == dummy_image.shape, "Output shape mismatch"
