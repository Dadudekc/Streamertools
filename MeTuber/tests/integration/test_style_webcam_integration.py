import pytest
import numpy as np
from src.core.style_manager import StyleManager
from src.services.webcam_service import WebcamService
from styles.base import Style

class MockStyle(Style):
    """Mock style class for testing."""
    def __init__(self):
        super().__init__()
        self.name = "mock_style"
        self.category = "test_category"
    
    def define_parameters(self):
        return [
            {"name": "param1", "type": "int", "min": 0, "max": 100, "default": 50},
            {"name": "param2", "type": "float", "min": 0.0, "max": 1.0, "default": 0.5}
        ]
    
    def apply(self, frame, params):
        return frame

@pytest.fixture
def style_manager():
    """Create a StyleManager instance."""
    return StyleManager()

@pytest.fixture
def webcam_service():
    """Create a WebcamService instance."""
    return WebcamService()

@pytest.fixture
def mock_frame():
    """Create a mock frame for testing."""
    return np.zeros((480, 640, 3), dtype=np.uint8)

def test_style_webcam_integration(style_manager, webcam_service, mock_frame):
    """Test integration between StyleManager and WebcamService."""
    # Create and register mock style
    mock_style = MockStyle()
    style_manager.style_instances["mock_style"] = mock_style
    
    # Get style parameters
    params = style_manager.get_default_parameters("mock_style")
    assert params["param1"] == 50
    assert params["param2"] == 0.5
    
    # Start webcam service with style
    assert webcam_service.start("test_device", mock_style, params)
    assert webcam_service._style_instance == mock_style
    assert webcam_service._style_params == params
    
    # Update parameters
    new_params = {"param1": 75, "param2": 0.8}
    validated_params = style_manager.validate_style_parameters("mock_style", new_params)
    webcam_service.update_parameters(validated_params)
    assert webcam_service._style_params == validated_params

def test_style_webcam_error_handling(style_manager, webcam_service):
    """Test error handling in style-webcam integration."""
    # Test with invalid style
    assert not webcam_service.start("test_device", None, {})
    
    # Test with invalid parameters
    mock_style = MockStyle()
    style_manager.style_instances["mock_style"] = mock_style
    
    invalid_params = {"param1": 150, "param2": 2.0}  # Out of range
    validated_params = style_manager.validate_style_parameters("mock_style", invalid_params)
    assert validated_params["param1"] == 100  # Clamped to max
    assert validated_params["param2"] == 1.0  # Clamped to max
    
    # Test style application error
    class ErrorStyle(MockStyle):
        def apply(self, frame, params):
            raise Exception("Style application error")
    
    error_style = ErrorStyle()
    style_manager.style_instances["error_style"] = error_style
    
    assert not webcam_service.start("test_device", error_style, {})

def test_style_webcam_parameter_validation(style_manager, webcam_service):
    """Test parameter validation in style-webcam integration."""
    # Create mock style
    mock_style = MockStyle()
    style_manager.style_instances["mock_style"] = mock_style
    
    # Test parameter types
    params = {
        "param1": "invalid",  # Should be int
        "param2": "invalid"   # Should be float
    }
    
    validated_params = style_manager.validate_style_parameters("mock_style", params)
    assert validated_params["param1"] == 50  # Default value
    assert validated_params["param2"] == 0.5  # Default value
    
    # Test missing parameters
    params = {}  # Empty parameters
    validated_params = style_manager.validate_style_parameters("mock_style", params)
    assert validated_params["param1"] == 50  # Default value
    assert validated_params["param2"] == 0.5  # Default value
    
    # Test extra parameters
    params = {
        "param1": 75,
        "param2": 0.8,
        "extra_param": "value"  # Should be ignored
    }
    validated_params = style_manager.validate_style_parameters("mock_style", params)
    assert "extra_param" not in validated_params
    assert validated_params["param1"] == 75
    assert validated_params["param2"] == 0.8 