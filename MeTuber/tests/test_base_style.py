# tests/test_base_style.py
import pytest
import numpy as np
from styles.base import Style
import time

class BaseStyleHelper(Style):
    """
    Helper class derived from Style for testing purposes.
    """
    name = "Test Style"
    category = "Test Category"

    def define_parameters(self):
        return [
            {"name": "int_param", "type": "int", "default": 5, "min": 1, "max": 10, "step": 1},
            {"name": "float_param", "type": "float", "default": 0.5, "min": 0.1, "max": 1.0, "step": 0.1},
            {"name": "str_param", "type": "str", "default": "option1", "options": ["option1", "option2", "option3"]},
        ]

    def apply(self, frame, params=None):
        """
        Apply the style to the given frame using the provided parameters.

        Args:
            frame (numpy.ndarray): The input video frame.
            params (dict, optional): Parameters for the style. Defaults to None.

        Returns:
            numpy.ndarray: The styled video frame.

        Raises:
            ValueError: If the frame is invalid or not a NumPy array.
        """
        if frame is None or not isinstance(frame, np.ndarray):
            raise ValueError("Invalid frame provided. Expected a NumPy array.")
        
        if len(frame.shape) not in [2, 3]:  # Ensure it's a valid image (2D grayscale or 3D RGB)
            raise ValueError("Invalid frame dimensions. Expected a 2D or 3D NumPy array.")

        # Use default parameters if params are not provided
        params = self.validate_params(params or {})
        return frame  # No-op for testing


def test_real_time_processing(dummy_image):
    """
    Test real-time processing by simulating multiple frames.
    """
    style = BaseStyleHelper()
    params = {
        "int_param": 6,
        "float_param": 0.7,
        "str_param": "option3"
    }

    frame_count = 100  # Simulate 100 frames
    start_time = time.time()

    for _ in range(frame_count):
        result = style.apply(dummy_image, params)
        assert isinstance(result, np.ndarray)
        assert result.shape == dummy_image.shape

    elapsed_time = time.time() - start_time
    avg_time_per_frame = elapsed_time / frame_count
    print(f"Processed {frame_count} frames in {elapsed_time:.2f} seconds (avg {avg_time_per_frame:.2f} seconds per frame).")

    # Assert that average processing time is below an acceptable threshold
    assert avg_time_per_frame < 0.05, "Processing time exceeds real-time threshold."

def test_parameter_boundaries(dummy_image):
    """
    Test parameter boundary conditions for the apply method.
    """
    style = BaseStyleHelper()

    # Test with minimum values
    min_params = {
        "int_param": 1,
        "float_param": 0.1,
        "str_param": "option1"
    }
    result = style.apply(dummy_image, min_params)
    assert isinstance(result, np.ndarray)

    # Test with maximum values
    max_params = {
        "int_param": 10,
        "float_param": 1.0,
        "str_param": "option3"
    }
    result = style.apply(dummy_image, max_params)
    assert isinstance(result, np.ndarray)

    # Test with out-of-range values (should raise ValueError)
    with pytest.raises(ValueError, match="Parameter 'int_param' must be between 1 and 10."):
        style.apply(dummy_image, {"int_param": 11})

    with pytest.raises(ValueError, match="Parameter 'float_param' must be between 0.1 and 1.0."):
        style.apply(dummy_image, {"float_param": 1.5})

    with pytest.raises(ValueError, match="Parameter 'str_param' must be one of"):
        style.apply(dummy_image, {"str_param": "invalid_option"})

@pytest.fixture
def dummy_image():
    """Fixture for creating a dummy image."""
    return np.ones((100, 100, 3), dtype=np.uint8) * 255


def test_validate_params():
    style = BaseStyleHelper()

    # Test valid parameters
    valid_params = {
        "int_param": 8,
        "float_param": 0.8,
        "str_param": "option2"
    }
    validated = style.validate_params(valid_params)
    assert validated == valid_params

    # Test invalid int_param (out of range)
    with pytest.raises(ValueError, match="Parameter 'int_param' must be between 1 and 10."):
        style.validate_params({"int_param": 15})

    # Test invalid float_param (out of range)
    with pytest.raises(ValueError, match="Parameter 'float_param' must be between 0.1 and 1.0."):
        style.validate_params({"float_param": 1.5})

    # Test invalid str_param (not in options)
    with pytest.raises(ValueError, match="Parameter 'str_param' must be one of"):
        style.validate_params({"str_param": "invalid_option"})


def test_apply(dummy_image):
    """
    Test the apply method.
    """
    style = BaseStyleHelper()

    # Test apply with valid parameters
    params = {
        "int_param": 6,
        "float_param": 0.7,
        "str_param": "option3"
    }
    result = style.apply(dummy_image, params)
    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape

    # Test apply with no parameters (use defaults)
    result = style.apply(dummy_image)
    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape

    # Test apply with invalid image (None)
    with pytest.raises(ValueError, match="Invalid frame provided. Expected a NumPy array."):
        style.apply(None)

    # Test apply with non-NumPy array
    with pytest.raises(ValueError, match="Invalid frame provided. Expected a NumPy array."):
        style.apply("invalid_image")

    # Test apply with incorrectly shaped NumPy array
    with pytest.raises(ValueError, match="Invalid frame dimensions. Expected a 2D or 3D NumPy array."):
        style.apply(np.array([1, 2, 3]))


def test_describe():
    style = BaseStyleHelper()
    description = style.describe()
    assert "Style: Test Style" in description
    assert "Category: Test Category" in description
    assert "- int_param: int" in description
    assert "- float_param: float" in description
    assert "- str_param: str" in description
