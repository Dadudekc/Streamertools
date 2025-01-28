import cv2
import numpy as np
import pytest
from adjustments.solarize import Solarize


@pytest.fixture
def dummy_image():
    """Generate a dummy image for testing."""
    return np.array([[100, 150], [200, 250]], dtype=np.uint8)


def test_solarize_default_threshold(dummy_image):
    solarize = Solarize()
    params = {"threshold": 128}
    result = solarize.apply(dummy_image, params)
    expected = np.array([[100, 105], [55, 5]], dtype=np.uint8)  # Inverted values above 128
    assert np.array_equal(result, expected), f"Expected {expected}, got {result}"


def test_solarize_custom_threshold():
    style = Solarize()
    input_image = np.array([[100, 150], [200, 50]], dtype=np.uint8)  # Example 2D array
    params = {"threshold": 128}
    expected_output = np.array([[100, 105], [55, 50]], dtype=np.uint8)
    output_image = style.apply(input_image, params)
    assert np.array_equal(output_image, expected_output), f"Got {output_image}, expected {expected_output}"
