import pytest
import cv2
import numpy as np
from unittest.mock import patch
from styles.artistic.pencil_sketch import PencilSketch

@pytest.fixture
def dummy_image():
    return np.ones((100, 100, 3), dtype=np.uint8) * 255

@patch("cv2.imshow", return_value=None)  # Mock imshow
@patch("cv2.waitKey", return_value=ord('q'))  # Mock waitKey
def test_webcam_pencil_sketch(mock_imshow, mock_waitkey, dummy_image):
    pencil_sketch = PencilSketch()
    params = {"blur_intensity": 15}
    sketch = pencil_sketch.apply(dummy_image, params)
    assert sketch is not None, "Sketch output is None"
    assert sketch.shape == dummy_image.shape[:2], "Output shape mismatch"

    # Simulate display logic (if needed for additional testing)
    cv2.imshow("Sketch", sketch)
    cv2.waitKey(1)
    cv2.destroyAllWindows()
