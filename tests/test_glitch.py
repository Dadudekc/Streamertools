import pytest
import numpy as np
from styles.distortions.glitch import Glitch

@pytest.fixture
def dummy_image():
    """
    Create a dummy image for testing purposes.
    """
    dummy_image = np.ones((100, 100, 3), dtype=np.uint8) * 255
    return dummy_image

def test_glitch_default_params(dummy_image):
    """
    Test the Glitch effect with default parameters.
    """
    glitch = Glitch()
    result = glitch.apply(dummy_image, {})
    assert result is not None, "The Glitch effect returned None."
    assert result.shape == dummy_image.shape, "Output shape mismatch."
    assert np.any(result != dummy_image), "The Glitch effect did not alter the image as expected."

def test_glitch_custom_params(dummy_image):
    """
    Test the Glitch effect with custom parameters.
    """
    glitch = Glitch()
    params = {"max_shift": 20, "num_shifts": 10}
    result = glitch.apply(dummy_image, params)
    assert result is not None, "The Glitch effect returned None with custom parameters."
    assert result.shape == dummy_image.shape, "Output shape mismatch with custom parameters."

def test_glitch_invalid_image():
    """
    Test the Glitch effect with invalid images.
    """
    glitch = Glitch()
    with pytest.raises(ValueError, match="Input image cannot be None."):
        glitch.apply(None, {})
    with pytest.raises(ValueError, match="Input image must be a BGR color image."):
        glitch.apply(np.ones((100, 100), dtype=np.uint8), {})

def test_glitch_invalid_params(dummy_image):
    """
    Test the Glitch effect with invalid parameters.
    """
    glitch = Glitch()
    with pytest.raises(ValueError, match="Parameter 'max_shift' must be between 0 and 50."):
        glitch.apply(dummy_image, {"max_shift": 100})
    with pytest.raises(ValueError, match="Parameter 'num_shifts' must be between 1 and 20."):
        glitch.apply(dummy_image, {"num_shifts": 25})
