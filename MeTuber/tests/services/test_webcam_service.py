import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from PyQt5.QtCore import QObject
from src.services.webcam_service import WebcamService
from styles.base import Style
from pyvirtualcam import PixelFormat
import av

class MockStyle(Style):
    """Mock style for testing."""
    def __init__(self):
        super().__init__()
        self.name = "MockStyle"
        self.category = "Test"

    def define_parameters(self):
        """Define test parameters."""
        return {
            "param1": {"default": 50, "min": 0, "max": 100},
            "param2": {"default": 0.5, "min": 0.0, "max": 1.0}
        }

    def apply(self, image, params=None):
        """Mock apply method."""
        return image

@pytest.fixture
def webcam_service():
    """Create a WebcamService instance for testing."""
    return WebcamService()

@pytest.fixture
def mock_frame():
    """Create a mock frame for testing."""
    return np.zeros((480, 640, 3), dtype=np.uint8)

def test_webcam_service_initialization(webcam_service):
    """Test WebcamService initialization."""
    assert webcam_service is not None
    assert isinstance(webcam_service, QObject)
    assert not webcam_service._is_running
    assert webcam_service._container is None
    assert webcam_service._camera is None
    assert webcam_service._style_instance is None
    assert webcam_service._style_params == {}
    assert webcam_service._input_device == ""

def test_webcam_service_start(webcam_service, mock_style, mock_frame):
    """Test starting the webcam service."""
    # Mock av.open
    with patch('av.open') as mock_av_open, \
         patch('pyvirtualcam.Camera') as mock_camera:
        
        # Set up mock container
        mock_container = MagicMock()
        mock_container.decode.return_value = [mock_frame]
        mock_av_open.return_value = mock_container
        
        # Set up mock camera
        mock_camera_instance = MagicMock()
        mock_camera.return_value = mock_camera_instance
        
        # Start service
        assert webcam_service.start("test_device", mock_style, {"param1": 50})
        assert webcam_service.is_running()
        assert webcam_service._style_instance == mock_style
        assert webcam_service._style_params == {"param1": 50}
        
        # Stop service
        webcam_service.stop()
        assert not webcam_service.is_running()

def test_webcam_service_stop(webcam_service, mock_frame):
    """Test stopping the webcam service."""
    # Setup mock objects
    mock_container = MagicMock()
    mock_container.decode.return_value = [MagicMock(to_ndarray=lambda: mock_frame)]
    mock_av_open.return_value = mock_container
    
    mock_camera_instance = MagicMock()
    mock_camera.return_value = mock_camera_instance
    
    # Start and then stop service
    webcam_service.start("test_device", MockStyle(), {})
    webcam_service.stop()
    
    assert not webcam_service._is_running
    assert webcam_service._container is None
    assert webcam_service._camera is None
    assert webcam_service._style_instance is None
    assert webcam_service._style_params == {}
    assert webcam_service._input_device == ""

def test_webcam_service_update_parameters(webcam_service):
    """Test updating style parameters."""
    webcam_service._style_params = {"old_param": 1}
    webcam_service.update_parameters({"new_param": 2})
    assert webcam_service._style_params == {"new_param": 2}

def test_webcam_service_get_last_frame(webcam_service, mock_frame):
    """Test getting the last processed frame."""
    # Test when no frame is available
    assert webcam_service.get_last_frame() is None
    
    # Test when frame is available
    webcam_service._last_frame = mock_frame
    assert np.array_equal(webcam_service.get_last_frame(), mock_frame)

def test_webcam_service_is_running(webcam_service):
    """Test checking if service is running."""
    assert not webcam_service.is_running()
    webcam_service._is_running = True
    assert webcam_service.is_running()

def test_webcam_service_error_handling(webcam_service, mock_style):
    """Test error handling in webcam service."""
    # Test device error
    with patch('av.open', side_effect=av.AVError("Device error")):
        assert not webcam_service.start("test_device", mock_style, {})
        assert not webcam_service.is_running()
    
    # Test camera error
    with patch('av.open') as mock_av_open, \
         patch('pyvirtualcam.Camera', side_effect=Exception("Camera error")):
        
        mock_container = MagicMock()
        mock_av_open.return_value = mock_container
        
        assert not webcam_service.start("test_device", mock_style, {})
        assert not webcam_service.is_running()
    
    # Test style error
    error_style = MagicMock()
    error_style.apply.side_effect = Exception("Style error")
    
    with patch('av.open') as mock_av_open, \
         patch('pyvirtualcam.Camera') as mock_camera:
        
        mock_container = MagicMock()
        mock_av_open.return_value = mock_container
        
        mock_camera_instance = MagicMock()
        mock_camera.return_value = mock_camera_instance
        
        assert webcam_service.start("test_device", error_style, {})
        assert webcam_service.is_running()
        
        # Stop service
        webcam_service.stop()
        assert not webcam_service.is_running() 