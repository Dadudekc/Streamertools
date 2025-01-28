import cv2
import numpy as np
import pytest
from adjustments.threshold import Threshold


@pytest.fixture
def dummy_image():
    """Generate a dummy grayscale image for testing."""
    return np.array([[50, 150], [200, 250]], dtype=np.uint8)


def test_threshold_default(dummy_image):
    threshold = Threshold()
    params = {"threshold": 128}
    result = threshold.apply(dummy_image, params)
    expected = np.array([[0, 255], [255, 255]], dtype=np.uint8)
    assert np.array_equal(result, expected), f"Expected {expected}, got {result}"


def test_threshold_custom(dummy_image):
    threshold = Threshold()
    params = {"threshold": 200}
    result = threshold.apply(dummy_image, params)
    expected = np.array([[0, 0], [255, 255]], dtype=np.uint8)
    assert np.array_equal(result, expected), f"Expected {expected}, got {result}"
