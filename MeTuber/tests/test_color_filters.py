import pytest
import numpy as np
from styles.color_filters import InvertColors, Negative, InvertFilter
import cv2

@pytest.fixture
def dummy_image():
    return np.full((100, 100, 3), 128, dtype=np.uint8)

def test_invert_colors_full_inversion(dummy_image):
    """
    Test full inversion with alpha = 1.0.
    """
    invert_colors = InvertColors()
    params = {"invert_alpha": 1.0}
    result = invert_colors.apply(dummy_image, params)

    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape
    assert np.array_equal(result, cv2.bitwise_not(dummy_image))

def test_invert_colors_partial_inversion(dummy_image):
    """
    Test partial inversion with alpha = 0.5.
    """
    invert_colors = InvertColors()
    params = {"invert_alpha": 0.5}
    result = invert_colors.apply(dummy_image, params)

    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape

    inverted = cv2.bitwise_not(dummy_image)
    blended = cv2.addWeighted(dummy_image, 0.5, inverted, 0.5, 0)
    assert np.array_equal(result, blended)

def test_negative(dummy_image):
    """
    Test the Negative effect.
    """
    negative = Negative()
    result = negative.apply(dummy_image)

    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape
    assert np.array_equal(result, cv2.bitwise_not(dummy_image))

def test_invert_filter(dummy_image):
    """
    Test the InvertFilter effect.
    """
    invert_filter = InvertFilter()
    result = invert_filter.apply(dummy_image)

    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape
    assert np.array_equal(result, cv2.bitwise_not(dummy_image))

def test_invalid_image_input():
    """
    Test handling of invalid image input.
    """
    invert_colors = InvertColors()
    with pytest.raises(ValueError, match="Invalid image provided. Expected a NumPy array."):
        invert_colors.apply(None)

    negative = Negative()
    with pytest.raises(ValueError, match="Invalid image provided. Expected a NumPy array."):
        negative.apply(None)

    invert_filter = InvertFilter()
    with pytest.raises(ValueError, match="Invalid image provided. Expected a NumPy array."):
        invert_filter.apply(None)
