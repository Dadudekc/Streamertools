import pytest
from unittest.mock import MagicMock, patch
from src.core.device_manager import DeviceManagerFactory, BaseDeviceManager

@pytest.fixture
def device_manager():
    """Create a DeviceManager instance."""
    return DeviceManagerFactory.create()

def test_device_manager_initialization(device_manager):
    """Test DeviceManager initialization."""
    assert device_manager is not None
    assert isinstance(device_manager, BaseDeviceManager)
    assert isinstance(device_manager._devices, list)

@patch('subprocess.check_output')
def test_device_manager_refresh_devices(mock_check_output, device_manager):
    """Test refreshing device list."""
    # Mock FFmpeg output
    mock_output = b"""[dshow @ 000001234567890] DirectShow video devices (some devices may be both video and audio devices)
[dshow @ 000001234567890]  "Integrated Camera"
[dshow @ 000001234567890]  "Logitech Webcam"
"""
    mock_check_output.return_value = mock_output
    
    device_manager.refresh_devices()
    assert len(device_manager._devices) > 0
    assert any(d["name"] == "Integrated Camera" for d in device_manager._devices)
    assert any(d["name"] == "Logitech Webcam" for d in device_manager._devices)

def test_device_manager_get_devices(device_manager):
    """Test getting available devices."""
    # Set up test devices
    device_manager._devices = [
        {"id": "video=Camera 1", "name": "Camera 1", "type": "video"},
        {"id": "video=Camera 2", "name": "Camera 2", "type": "video"}
    ]
    devices = device_manager.get_devices()
    assert isinstance(devices, list)
    assert len(devices) == 2
    assert all(isinstance(d, dict) for d in devices)
    assert all(all(k in d for k in ["id", "name", "type"]) for d in devices)
    assert devices == device_manager._devices

def test_device_manager_get_default_device(device_manager):
    """Test getting default device."""
    # Test with no devices
    device_manager._devices = []
    assert device_manager.get_device_info("") is None
    
    # Test with devices
    device_manager._devices = [
        {"id": "video=Camera 1", "name": "Camera 1", "type": "video"},
        {"id": "video=Camera 2", "name": "Camera 2", "type": "video"}
    ]
    info = device_manager.get_device_info("video=Camera 1")
    assert info is not None
    assert info["name"] == "Camera 1"

@patch('av.open')
def test_device_manager_validate_device(mock_av_open, device_manager):
    """Test device validation."""
    # Mock device list
    device_manager._devices = [
        {"id": "video=valid_camera", "name": "valid_camera", "type": "video"}
    ]
    
    # Test valid device
    assert device_manager.get_device_info("video=valid_camera") is not None
    
    # Test invalid device
    assert device_manager.get_device_info("video=invalid_camera") is None
    
    # Test empty device
    assert device_manager.get_device_info("") is None

@patch('av.open')
def test_device_manager_get_device_info(mock_av_open, device_manager):
    """Test getting device information."""
    # Mock device list
    device_manager._devices = [
        {"id": "video=valid_camera", "name": "valid_camera", "type": "video"}
    ]
    
    # Test with valid device
    info = device_manager.get_device_info("video=valid_camera")
    assert info is not None
    assert info["name"] == "valid_camera"
    assert info["type"] == "video"
    
    # Test with invalid device
    assert device_manager.get_device_info("video=invalid_camera") is None

def test_device_manager_factory():
    """Test DeviceManagerFactory."""
    manager = DeviceManagerFactory.create()
    assert isinstance(manager, BaseDeviceManager) 