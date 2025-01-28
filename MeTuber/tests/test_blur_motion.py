import pytest
import numpy as np
from styles.effects.blur_motion import BlurMotion

@pytest.fixture
def dummy_image():
    """Fixture for creating a dummy image."""
    return np.ones((100, 100, 3), dtype=np.uint8) * 255


def test_blur_motion_default_params(dummy_image):
    """
    Test the BlurMotion effect with default parameters.
    """
    blur_motion = BlurMotion()

    # Apply motion blur with default parameters
    result = blur_motion.apply(dummy_image)
    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape


def test_blur_motion_custom_params(dummy_image):
    """
    Test the BlurMotion effect with custom parameters.
    """
    blur_motion = BlurMotion()
    params = {"kernel_size": 25, "angle": 45}

    # Apply motion blur with custom parameters
    result = blur_motion.apply(dummy_image, params)
    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape


def test_blur_motion_invalid_image():
    """
    Test BlurMotion with invalid image input.
    """
    blur_motion = BlurMotion()

    # Test with None as the image
    with pytest.raises(ValueError, match="Invalid image provided. Expected a NumPy array."):
        blur_motion.apply(None)


def test_blur_motion_invalid_params(dummy_image):
    """
    Test BlurMotion with invalid parameters.
    """
    blur_motion = BlurMotion()

    # Test with invalid kernel_size (too large)
    with pytest.raises(ValueError, match="Parameter 'kernel_size' must be between 3 and 51."):
        blur_motion.apply(dummy_image, {"kernel_size": 100})

    # Test with invalid angle (out of range)
    with pytest.raises(ValueError, match="Parameter 'angle' must be between 0 and 360."):
        blur_motion.apply(dummy_image, {"angle": 400})


def test_blur_motion_kernel_adjustment(dummy_image):
    """
    Test BlurMotion kernel size adjustment for even values.
    """
    blur_motion = BlurMotion()

    # Test with an even kernel size
    params = {"kernel_size": 16, "angle": 0}  # kernel_size is even
    result = blur_motion.apply(dummy_image, params)
    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape  # Fixed variable name
