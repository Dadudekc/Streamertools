import pytest
import numpy as np
import cv2
from styles.effects.lines import HoughLines, CannyEdge


@pytest.fixture
def dummy_image():
    return np.zeros((100, 100, 3), dtype=np.uint8)


def test_hough_lines_default_params(dummy_image):
    hough_lines = HoughLines()
    result = hough_lines.apply(dummy_image)
    assert result is not None, "HoughLines returned None."
    assert result.shape == dummy_image.shape, "Output shape mismatch."


def test_hough_lines_invalid_image():
    hough_lines = HoughLines()
    with pytest.raises(ValueError, match="Input image cannot be None."):
        hough_lines.apply(None)


def test_canny_edge_default_params(dummy_image):
    canny_edge = CannyEdge()
    result = canny_edge.apply(dummy_image)
    assert result is not None, "CannyEdge returned None."
    assert result.shape == dummy_image.shape[:2], "Output shape mismatch."


def test_canny_edge_invalid_image():
    canny_edge = CannyEdge()
    with pytest.raises(ValueError, match="Input image cannot be None."):
        canny_edge.apply(None)

def test_canny_edge_invalid_aperture_size(dummy_image):
    canny_edge = CannyEdge()
    with pytest.raises(ValueError, match="Aperture size must be an odd number between 3 and 7."):
        canny_edge.apply(dummy_image, {"apertureSize": 4})
    with pytest.raises(ValueError, match="Aperture size must be an odd number between 3 and 7."):
        canny_edge.apply(dummy_image, {"apertureSize": 8})