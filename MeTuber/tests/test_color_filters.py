import pytest
import numpy as np
from styles.color_filters.negative import Negative
from styles.color_filters.invert_colors import InvertColors
from styles.color_filters.invert_filter import InvertFilter
import cv2

@pytest.fixture
def dummy_image():
    return np.full((100, 100, 3), 128, dtype=np.uint8)

def test_invert_colors_default_params(dummy_image):
    invert_colors = InvertColors()
    result = invert_colors.apply(dummy_image)
    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape
    assert np.array_equal(result, cv2.bitwise_not(dummy_image))

def test_invert_colors_full_inversion(dummy_image):
    invert_colors = InvertColors()
    params = {"invert_alpha": 1.0}
    result = invert_colors.apply(dummy_image, params)
    assert np.array_equal(result, cv2.bitwise_not(dummy_image))

def test_invert_colors_partial_inversion(dummy_image):
    invert_colors = InvertColors()
    params = {"invert_alpha": 0.5}
    result = invert_colors.apply(dummy_image, params)
    inverted = cv2.bitwise_not(dummy_image)
    blended = cv2.addWeighted(dummy_image, 0.5, inverted, 0.5, 0)

    # Use np.allclose for tolerance-based comparison
    assert np.allclose(result, blended, atol=1)


def test_negative(dummy_image):
    negative = Negative()
    result = negative.apply(dummy_image)
    assert np.array_equal(result, cv2.bitwise_not(dummy_image))

def test_invert_filter(dummy_image):
    invert_filter = InvertFilter()
    result = invert_filter.apply(dummy_image)
    assert np.array_equal(result, cv2.bitwise_not(dummy_image))

def test_invalid_image_input():
    invert_colors = InvertColors()
    with pytest.raises(ValueError, match="Input image cannot be None."):
        invert_colors.apply(None)

