import pytest
import numpy as np
from styles.basic.sepia_vibrant import SepiaVibrant

@pytest.fixture
def dummy_image():
    """Fixture for creating a dummy image."""
    return np.ones((100, 100, 3), dtype=np.uint8) * 128  # Gray image


def test_sepia_vibrant_default_params(dummy_image):
    """
    Test SepiaVibrant with default parameters.
    """
    sepia_vibrant = SepiaVibrant()

    # Apply with default parameters
    result = sepia_vibrant.apply(dummy_image)
    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape
    # Ensure the image is modified
    assert not np.array_equal(result, dummy_image)


def test_sepia_vibrant_custom_params(dummy_image):
    """
    Test SepiaVibrant with custom parameters.
    """
    sepia_vibrant = SepiaVibrant()
    params = {"sepia_intensity": 1.5, "vibrance": 2.0}

    # Apply with custom parameters
    result = sepia_vibrant.apply(dummy_image, params)
    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape
    # Ensure the image is modified differently than the default
    default_result = sepia_vibrant.apply(dummy_image)
    assert not np.array_equal(result, default_result)


def test_sepia_vibrant_zero_intensity(dummy_image):
    """
    Test SepiaVibrant with zero sepia intensity (no sepia effect).
    """
    sepia_vibrant = SepiaVibrant()
    params = {"sepia_intensity": 0.0, "vibrance": 1.0}

    # Apply with zero sepia intensity
    result = sepia_vibrant.apply(dummy_image, params)
    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape
    # Ensure the image is different because vibrance might still modify it
    assert not np.array_equal(result, dummy_image)


def test_sepia_vibrant_high_vibrance(dummy_image):
    """
    Test SepiaVibrant with high vibrance.
    """
    sepia_vibrant = SepiaVibrant()
    params = {"sepia_intensity": 1.0, "vibrance": 3.0}

    # Apply with high vibrance
    result = sepia_vibrant.apply(dummy_image, params)
    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape
    # Ensure the image is modified
    assert not np.array_equal(result, dummy_image)


def test_sepia_vibrant_invalid_image():
    """
    Test SepiaVibrant with invalid image input.
    """
    sepia_vibrant = SepiaVibrant()

    # Test with None as the image
    with pytest.raises(ValueError, match="Input image cannot be None."):
        sepia_vibrant.apply(None)
