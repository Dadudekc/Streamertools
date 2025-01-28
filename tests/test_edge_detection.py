import pytest
import numpy as np
from styles.artistic.edge_detection import EdgeDetection
import cv2

@pytest.fixture
def dummy_image():
    """
    Create a dummy image for testing purposes.
    """
    dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
    dummy_image = cv2.rectangle(dummy_image, (25, 25), (75, 75), (255, 255, 255), -1)
    return dummy_image

def test_edge_detection_default_params(dummy_image):
    """
    Test the EdgeDetection style with default parameters.
    """
    edge_detection = EdgeDetection()
    result = edge_detection.apply(dummy_image, {})
    assert result is not None, "The EdgeDetection effect returned None."
    assert result.shape == dummy_image.shape[:2], "Output shape mismatch."

def test_edge_detection_custom_params(dummy_image):
    """
    Test the EdgeDetection style with custom parameters.
    """
    edge_detection = EdgeDetection()
    params = {"threshold1": 50, "threshold2": 150}
    result = edge_detection.apply(dummy_image, params)
    assert result is not None, "The EdgeDetection effect returned None with custom parameters."
    assert result.shape == dummy_image.shape[:2], "Output shape mismatch with custom parameters."

def test_edge_detection_invalid_image():
    """
    Test the EdgeDetection style with invalid images.
    """
    edge_detection = EdgeDetection()
    with pytest.raises(ValueError, match="Input image cannot be None."):
        edge_detection.apply(None, {})
    with pytest.raises(ValueError, match="Input image must be a BGR color image."):
        edge_detection.apply(np.ones((100, 100), dtype=np.uint8), {})

def test_edge_detection_invalid_params(dummy_image):
    """
    Test the EdgeDetection style with invalid parameters.
    """
    edge_detection = EdgeDetection()
    with pytest.raises(ValueError, match="Parameter 'threshold1' must be between 0 and 500."):
        edge_detection.apply(dummy_image, {"threshold1": -10})
    with pytest.raises(ValueError, match="Parameter 'threshold2' must be between 0 and 500."):
        edge_detection.apply(dummy_image, {"threshold2": 600})
