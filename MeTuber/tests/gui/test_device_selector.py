import pytest
from PyQt5.QtWidgets import QApplication
from src.gui.components.device_selector import DeviceSelector

@pytest.fixture
def device_selector(qtbot):
    """Create a DeviceSelector instance."""
    devices = [
        {"name": "Camera 1", "id": "camera1"},
        {"name": "Camera 2", "id": "camera2"}
    ]
    selector = DeviceSelector(None, devices, "camera1")
    qtbot.addWidget(selector)
    return selector

def test_device_selector_initialization(device_selector):
    """Test device selector initialization."""
    assert device_selector is not None
    assert device_selector.device_combo is not None
    assert device_selector.device_combo.count() == 2
    assert device_selector.device_combo.currentData() == "camera1"

def test_device_selector_get_selected_device(device_selector):
    """Test getting the selected device."""
    assert device_selector.get_selected_device() == "camera1"
    device_selector.device_combo.setCurrentIndex(1)
    assert device_selector.get_selected_device() == "camera2"

def test_device_selector_set_available_devices(device_selector):
    """Test setting available devices."""
    new_devices = [
        {"name": "Camera 3", "id": "camera3"},
        {"name": "Camera 4", "id": "camera4"}
    ]
    device_selector.set_available_devices(new_devices)
    assert device_selector.device_combo.count() == 2
    assert device_selector.device_combo.itemText(0) == "Camera 3"
    assert device_selector.device_combo.itemText(1) == "Camera 4"
    assert device_selector.device_combo.itemData(0) == "camera3"
    assert device_selector.device_combo.itemData(1) == "camera4"

def test_device_selector_refresh_devices(device_selector):
    """Test refreshing devices."""
    device_selector.refresh_devices()
    assert device_selector.device_combo.count() == 2
    assert device_selector.device_combo.currentData() == "camera1"

def test_device_selector_error_handling(device_selector):
    """Test error handling."""
    # Test with invalid device list
    device_selector.set_available_devices(None)
    assert device_selector.device_combo.count() == 0
    assert device_selector.get_selected_device() == "" 