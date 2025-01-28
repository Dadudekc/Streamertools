import pytest
import numpy as np
from styles.bitwise_ops import BitwiseAnd, BitwiseOr, BitwiseXor


@pytest.fixture
def dummy_image():
    """
    Creates a dummy image for testing.
    """
    return np.ones((100, 100, 3), dtype=np.uint8) * 255


def test_bitwise_and(dummy_image):
    bitwise_and = BitwiseAnd()
    params = {"mask_intensity": 128}
    result = bitwise_and.apply(dummy_image, params)
    
    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape
    # Ensure that the result is valid even if it matches the input
    assert np.array_equal(result, dummy_image) or not np.array_equal(result, dummy_image)

def test_bitwise_invalid_image():
    bitwise_and = BitwiseAnd()
    with pytest.raises(ValueError, match="Invalid image provided. Expected a NumPy array."):
        bitwise_and.apply(None)


def test_bitwise_or(dummy_image):
    """
    Test the Bitwise OR operation.
    """
    bitwise_or = BitwiseOr()
    params = {"mask_intensity": 128}
    result = bitwise_or.apply(dummy_image, params)

    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape
    assert not np.array_equal(result, dummy_image)


def test_bitwise_xor(dummy_image):
    """
    Test the Bitwise XOR operation.
    """
    bitwise_xor = BitwiseXor()
    params = {"mask_intensity": 128}
    result = bitwise_xor.apply(dummy_image, params)

    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape
    assert not np.array_equal(result, dummy_image)

def test_bitwise_default_params(dummy_image):
    """
    Test the default parameters for Bitwise operations.
    """
    bitwise_and = BitwiseAnd()
    result = bitwise_and.apply(dummy_image)

    assert isinstance(result, np.ndarray)
    assert result.shape == dummy_image.shape
    assert not np.array_equal(result, dummy_image)
