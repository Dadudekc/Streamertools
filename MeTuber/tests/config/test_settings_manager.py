import os
import json
import pytest
from src.config.settings_manager import SettingsManager

@pytest.fixture
def settings_manager(tmp_path):
    """Create a SettingsManager instance with a temporary config file."""
    config_file = tmp_path / "test_config.json"
    return SettingsManager(str(config_file))

def test_settings_manager_initialization(settings_manager):
    """Test SettingsManager initialization with default settings."""
    assert settings_manager.settings is not None
    assert "input_device" in settings_manager.settings
    assert "style" in settings_manager.settings
    assert "parameters" in settings_manager.settings
    assert "log_level" in settings_manager.settings
    assert "virtual_camera" in settings_manager.settings

def test_settings_manager_save_load(settings_manager, tmp_path):
    """Test saving and loading settings."""
    # Modify some settings
    settings_manager.settings["input_device"] = "test_device"
    settings_manager.settings["style"] = "test_style"
    
    # Save settings
    assert settings_manager.save_settings()
    
    # Create new instance to load settings
    new_manager = SettingsManager(str(tmp_path / "test_config.json"))
    assert new_manager.settings["input_device"] == "test_device"
    assert new_manager.settings["style"] == "test_style"

def test_settings_manager_get_setting(settings_manager):
    """Test getting individual settings."""
    assert settings_manager.get_setting("input_device") == ""
    assert settings_manager.get_setting("style") == "Original"
    assert settings_manager.get_setting("nonexistent", "default") == "default"

def test_settings_manager_set_setting(settings_manager):
    """Test setting individual settings."""
    assert settings_manager.set_setting("input_device", "new_device")
    assert settings_manager.settings["input_device"] == "new_device"
    
    # Test setting invalid key
    assert not settings_manager.set_setting("", "value")

def test_settings_manager_style_parameters(settings_manager):
    """Test style parameter management."""
    style_name = "test_style"
    params = {"param1": 1, "param2": 2}
    
    # Set parameters
    assert settings_manager.set_style_parameters(style_name, params)
    assert settings_manager.get_style_parameters(style_name) == params
    
    # Get parameters for nonexistent style
    assert settings_manager.get_style_parameters("nonexistent") == {}

def test_settings_manager_reset_to_defaults(settings_manager):
    """Test resetting settings to defaults."""
    # Modify settings
    settings_manager.settings["input_device"] = "test_device"
    settings_manager.settings["style"] = "test_style"
    
    # Reset to defaults
    assert settings_manager.reset_to_defaults()
    assert settings_manager.settings["input_device"] == ""
    assert settings_manager.settings["style"] == "Original"

def test_settings_manager_validate_settings(settings_manager):
    """Test settings validation."""
    # Remove a required key
    del settings_manager.settings["input_device"]
    
    # Validate should restore missing keys
    assert settings_manager.validate_settings()
    assert "input_device" in settings_manager.settings 