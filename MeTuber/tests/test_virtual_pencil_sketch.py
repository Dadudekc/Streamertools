import pytest
import cv2
import numpy as np
from styles.artistic.pencil_sketch import PencilSketch


@pytest.fixture
def dummy_image():
    """Create a dummy image for testing."""
    image = np.ones((100, 100, 3), dtype=np.uint8) * 255
    cv2.rectangle(image, (25, 25), (75, 75), (0, 0, 0), -1)
    return image


def test_pencil_sketch_default_params(dummy_image):
    """Test PencilSketch with default parameters."""
    pencil_sketch = PencilSketch()
    result = pencil_sketch.apply(dummy_image)
    assert result is not None, "Result should not be None."
    assert result.shape[:2] == dummy_image.shape[:2], "Output dimensions should match input."
    assert len(result.shape) == 2, "Output should be a grayscale image."


def test_pencil_sketch_custom_params(dummy_image):
    """Test PencilSketch with custom parameters."""
    pencil_sketch = PencilSketch()
    params = {"blur_intensity": 15}
    result = pencil_sketch.apply(dummy_image, params)
    assert result is not None, "Result should not be None."
    assert result.shape[:2] == dummy_image.shape[:2], "Output dimensions should match input."


def test_pencil_sketch_even_blur(dummy_image):
    """Test PencilSketch with an even blur intensity, which should be adjusted to the next odd value."""
    pencil_sketch = PencilSketch()
    params = {"blur_intensity": 20}  # Even number
    result = pencil_sketch.apply(dummy_image, params)
    assert result is not None, "Result should not be None."


def test_pencil_sketch_invalid_image():
    """Test PencilSketch with an invalid input image."""
    pencil_sketch = PencilSketch()
    with pytest.raises(ValueError, match="Input image cannot be None."):
        pencil_sketch.apply(None)


def test_pencil_sketch_out_of_range_params(dummy_image):
    """Test PencilSketch with out-of-range parameters."""
    pencil_sketch = PencilSketch()

    # Test below the minimum value
    with pytest.raises(ValueError, match="Parameter 'blur_intensity' must be between 1 and 51."):
        pencil_sketch.apply(dummy_image, {"blur_intensity": 0})

    # Test above the maximum value
    with pytest.raises(ValueError, match="Parameter 'blur_intensity' must be between 1 and 51."):
        pencil_sketch.apply(dummy_image, {"blur_intensity": 60})


def test_pencil_sketch_missing_params(dummy_image):
    """Test PencilSketch with missing parameters."""
    pencil_sketch = PencilSketch()
    result = pencil_sketch.apply(dummy_image, params={})
    assert result is not None, "Result should not be None."
