import pytest
import numpy as np
from styles.basic.contrast_only import ContrastOnly


@pytest.fixture
def dummy_image():
    """Fixture for creating a dummy image."""
    return np.ones((100, 100, 3), dtype=np.uint8) * 128


def test_contrast_only_default_params(dummy_image):
    """
    Test ContrastOnly with default parameters.
    """
    contrast_only = ContrastOnly()

    # Apply with default parameters
    result = contrast_only.apply(dummy_image)
    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape
    # Ensure the image remains unchanged with default contrast=1.0
    assert np.array_equal(result, dummy_image)

    # Apply with modified contrast
    params = {"contrast": 2.0}
    result_modified = contrast_only.apply(dummy_image, params)
    assert isinstance(result_modified, np.ndarray)
    assert result_modified.shape == dummy_image.shape
    # Ensure the image is modified with contrast != 1.0
    assert not np.array_equal(result_modified, dummy_image)



def test_contrast_only_custom_params(dummy_image):
    """
    Test ContrastOnly with custom parameters.
    """
    contrast_only = ContrastOnly()

    # Apply with custom contrast
    params = {"contrast": 2.0}
    result = contrast_only.apply(dummy_image, params)
    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape
    assert not np.array_equal(result, dummy_image)  # Ensure the image is modified


def test_contrast_only_invalid_params(dummy_image):
    """
    Test ContrastOnly with invalid parameters.
    """
    contrast_only = ContrastOnly()

    # Test with contrast out of range (too high)
    with pytest.raises(ValueError, match="Parameter 'contrast' must be between 0.5 and 3.0."):
        contrast_only.apply(dummy_image, {"contrast": 5.0})

    # Test with contrast out of range (too low)
    with pytest.raises(ValueError, match="Parameter 'contrast' must be between 0.5 and 3.0."):
        contrast_only.apply(dummy_image, {"contrast": 0.2})


def test_contrast_only_invalid_image():
    """
    Test ContrastOnly with invalid image input.
    """
    contrast_only = ContrastOnly()

    # Test with None as the image
    with pytest.raises(ValueError, match="Input image cannot be None."):
        contrast_only.apply(None)


def test_contrast_only_no_change(dummy_image):
    """
    Test ContrastOnly with a contrast of 1.0 (no change).
    """
    contrast_only = ContrastOnly()
    params = {"contrast": 1.0}

    # Apply with no contrast change
    result = contrast_only.apply(dummy_image, params)
    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape
    assert np.array_equal(result, dummy_image)  # Ensure the image remains the same
