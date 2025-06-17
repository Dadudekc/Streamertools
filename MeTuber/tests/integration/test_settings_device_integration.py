import pytest
import os
from src.config.settings_manager import SettingsManager
from src.core.device_manager import DeviceManagerFactory

@pytest.fixture
def settings_manager(tmp_path):
    """Create a SettingsManager instance with a temporary config file."""
    config_file = tmp_path / "test_config.json"
    return SettingsManager(str(config_file))

@pytest.fixture
def device_manager():
    """Create a DeviceManager instance."""
    return DeviceManagerFactory.create()

def test_settings_device_integration(settings_manager, device_manager):
    """Test integration between SettingsManager and DeviceManager."""
    # Get available devices
    devices = device_manager.get_devices()
    
    if devices:  # Only run if there are actual devices
        # Save a device to settings
        test_device = devices[0]["id"]
        settings_manager.set_setting("input_device", test_device)
        settings_manager.save_settings()
        
        # Verify device is valid
        assert device_manager.validate_device(test_device)
        
        # Get device info
        device_info = device_manager.get_device_info(test_device)
        assert device_info is not None
        assert "name" in device_info
        assert "id" in device_info
        assert "type" in device_info
        
        # Update settings with device info
        settings_manager.set_setting("device_info", device_info)
        settings_manager.save_settings()
        
        # Load settings and verify device info
        loaded_info = settings_manager.get_setting("device_info")
        assert loaded_info == device_info

def test_settings_device_error_handling(settings_manager, device_manager):
    """Test error handling in settings-device integration."""
    # Test with invalid device
    settings_manager.set_setting("input_device", "invalid_device")
    settings_manager.save_settings()
    
    # Verify device validation fails
    assert not device_manager.validate_device("invalid_device")
    
    # Test with empty device
    settings_manager.set_setting("input_device", "")
    settings_manager.save_settings()
    
    # Verify empty device handling
    assert not device_manager.validate_device("")
    
    # Test device info for invalid device
    assert device_manager.get_device_info("invalid_device") is None

def test_settings_device_persistence(settings_manager, device_manager, tmp_path):
    """Test persistence of device settings."""
    # Get available devices
    devices = device_manager.get_devices()
    
    if devices:
        # Save device and info
        test_device = devices[0]["id"]
        device_info = device_manager.get_device_info(test_device)
        
        settings_manager.set_setting("input_device", test_device)
        settings_manager.set_setting("device_info", device_info)
        settings_manager.save_settings()
        
        # Create new instances
        new_settings = SettingsManager(str(tmp_path / "test_config.json"))
        new_device = DeviceManagerFactory.create()
        
        # Verify settings persistence
        assert new_settings.get_setting("input_device") == test_device
        assert new_settings.get_setting("device_info") == device_info
        
        # Verify device still valid
        assert new_device.validate_device(test_device)
        assert new_device.get_device_info(test_device) == device_info 