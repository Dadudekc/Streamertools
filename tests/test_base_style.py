import pytest
import numpy as np
from styles.base import Style


class BaseStyleHelper(Style):
    """
    Helper class derived from Style for testing purposes.
    """
    name = "Test Style"
    category = "Test Category"
    parameters = [
        {"name": "int_param", "type": "int", "default": 5, "min": 1, "max": 10, "step": 1},
        {"name": "float_param", "type": "float", "default": 0.5, "min": 0.1, "max": 1.0, "step": 0.1},
        {"name": "str_param", "type": "str", "default": "option1", "options": ["option1", "option2", "option3"]},
    ]


@pytest.fixture
def dummy_image():
    """Fixture for creating a dummy image."""
    return np.ones((100, 100, 3), dtype=np.uint8) * 255


def test_validate_params():
    """
    Test parameter validation for various scenarios.
    """
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

    # Test apply with invalid image
    with pytest.raises(ValueError, match="Invalid image provided. Expected a NumPy array."):
        style.apply(None)


def test_describe():
    """
    Test the describe method.
    """
    style = BaseStyleHelper()
    description = style.describe()
    assert "Style: Test Style" in description
    assert "Category: Test Category" in description
    assert "- int_param: int" in description
    assert "- float_param: float" in description
    assert "- str_param: str" in description
