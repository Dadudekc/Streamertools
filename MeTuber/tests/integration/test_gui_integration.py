import pytest
import numpy as np
from PyQt5.QtWidgets import QApplication
from unittest.mock import MagicMock, patch
from src.gui.main_window import MainWindow
from src.config.settings_manager import SettingsManager
from src.core.device_manager import DeviceManagerFactory
from src.core.style_manager import StyleManager
from src.services.webcam_service import WebcamService
from src.gui.components.device_selector import DeviceSelector
from src.gui.components.style_tab_manager import StyleTabManager

class MockStyle:
    """Mock style class for testing."""
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.parameters = [
            {"name": "param1", "type": "int", "min": 0, "max": 100, "default": 50}
        ]
    
    def apply(self, frame, params):
        return frame
        
    def define_parameters(self):
        return self.parameters

@pytest.fixture(scope="module")
def qapp():
    """Create a QApplication instance."""
    app = QApplication([])
    yield app
    app.quit()

@pytest.fixture
def mock_managers():
    """Create mock manager instances."""
    with patch('src.config.settings_manager.SettingsManager') as mock_settings, \
         patch('src.core.device_manager.DeviceManagerFactory') as mock_device_factory, \
         patch('src.core.style_manager.StyleManager') as mock_style, \
         patch('src.services.webcam_service.WebcamService') as mock_webcam:
        
        # Setup mock managers
        mock_settings.return_value = MagicMock(spec=SettingsManager)
        mock_device = MagicMock()
        mock_device_factory.create.return_value = mock_device
        mock_style.return_value = MagicMock(spec=StyleManager)
        mock_webcam.return_value = MagicMock(spec=WebcamService)
        
        yield {
            'settings': mock_settings.return_value,
            'device': mock_device,
            'style': mock_style.return_value,
            'webcam': mock_webcam.return_value
        }

@pytest.fixture
def main_window(qapp, mock_managers, qtbot):
    """Create a MainWindow instance with proper cleanup."""
    window = MainWindow()
    window.device_manager = mock_managers['device']
    window.style_manager = mock_managers['style']
    window.webcam_service = mock_managers['webcam']
    window.settings_manager = mock_managers['settings']
    qtbot.addWidget(window)
    yield window
    try:
        # Disconnect signals before cleanup
        if window.webcam_service:
            try:
                window.webcam_service.error_signal.disconnect()
                window.webcam_service.info_signal.disconnect()
                window.webcam_service.frame_ready.disconnect()
            except (TypeError, RuntimeError):
                pass  # Ignore errors if signals are already disconnected
        
        # Clean up components
        if window.device_selector:
            window.device_selector.deleteLater()
        if window.style_tab_manager:
            window.style_tab_manager.deleteLater()
        if window.parameter_controls:
            window.parameter_controls.deleteLater()
        if window.action_buttons:
            window.action_buttons.deleteLater()
        if window.preview_label:
            window.preview_label.deleteLater()
        if window.status_label:
            window.status_label.deleteLater()
            
        # Clear references
        window.device_selector = None
        window.style_tab_manager = None
        window.parameter_controls = None
        window.action_buttons = None
        window.preview_label = None
        window.status_label = None
        
        # Close and delete window
        window.close()
        window.deleteLater()
        
    except Exception as e:
        print(f"Error during cleanup: {e}")

def test_gui_device_integration(main_window, mock_managers, qtbot):
    """Test integration between GUI and device management."""
    # Mock device list
    mock_managers['device'].get_devices.return_value = ["Camera 1", "Camera 2"]
    mock_managers['device'].get_default_device.return_value = "Camera 1"
    
    # Initialize device selector
    device_selector = DeviceSelector(main_window, ["Camera 1", "Camera 2"], "Camera 1")
    qtbot.addWidget(device_selector)
    main_window.device_selector = device_selector
    
    # Test device selection
    assert device_selector.get_selected_device() == "Camera 1"
    device_selector.device_combo.setCurrentText("Camera 2")
    assert device_selector.get_selected_device() == "Camera 2"
    
    # Test device validation
    mock_managers['device'].validate_device.return_value = True
    assert main_window.start_virtual_camera()
    
    mock_managers['device'].validate_device.return_value = False
    assert not main_window.start_virtual_camera()

def test_gui_style_integration(main_window, mock_managers, qtbot):
    """Test integration between GUI and style management."""
    # Mock style data
    mock_style = MockStyle("test_style", "test_category")
    mock_managers['style'].get_style.return_value = mock_style
    mock_managers['style'].get_categories.return_value = {
        "test_category": ["test_style"]
    }
    
    try:
        # Initialize style tab manager
        style_tab_manager = StyleTabManager(
            main_window,
            {"test_category": ["test_style"]},
            {"test_style": mock_style},
            {}
        )
        qtbot.addWidget(style_tab_manager)
        main_window.style_tab_manager = style_tab_manager
        
        # Test style selection
        assert style_tab_manager.set_current_style("test_style")
        assert style_tab_manager.get_current_style() == "test_style"
        
        # Set style in parameter controls
        main_window.parameter_controls.set_style(mock_style)
        
        # Test parameter updates
        mock_managers['style'].validate_style_parameters.return_value = {"param1": 75}
        mock_managers['webcam'].update_parameters.return_value = True
        main_window.parameter_controls.set_parameters({"param1": 75})
        assert mock_managers['webcam'].update_parameters.called
        
    finally:
        # Clean up
        if style_tab_manager:
            style_tab_manager.deleteLater()
            main_window.style_tab_manager = None

def test_gui_webcam_integration(main_window, mock_managers, qtbot):
    """Test integration between GUI and webcam service."""
    # Mock frame
    mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    mock_managers['webcam'].get_last_frame.return_value = mock_frame
    
    # Test preview updates
    main_window.update_preview(mock_frame)
    assert main_window.preview_label.pixmap() is not None
    
    # Test snapshot functionality
    with patch('cv2.imwrite') as mock_imwrite:
        main_window.take_snapshot()
        mock_imwrite.assert_called_once()
    
    # Test start/stop functionality
    mock_managers['webcam'].start.return_value = True
    assert main_window.start_virtual_camera()
    assert main_window.status_label.text() == "Status: Running"
    
    main_window.stop_virtual_camera()
    assert main_window.status_label.text() == "Status: Idle"

def test_gui_settings_integration(main_window, mock_managers, qtbot):
    """Test integration between GUI and settings management."""
    # Mock settings
    mock_managers['settings'].get_setting.side_effect = lambda key: {
        "input_device": "test_device",
        "style": "test_style",
        "parameters": {"param1": 50}
    }.get(key, None)
    
    # Test settings loading
    main_window.load_settings()
    mock_managers['settings'].get_setting.assert_called()
    
    # Test settings saving
    main_window.save_settings()
    mock_managers['settings'].set_setting.assert_called()
    mock_managers['settings'].save_settings.assert_called()

def test_gui_error_handling(main_window, mock_managers, qtbot):
    """Test error handling in GUI integration."""
    # Test device errors
    mock_managers['device'].validate_device.side_effect = Exception("Device Error")
    main_window.start_virtual_camera()
    assert "Error" in main_window.status_label.text()
    
    # Test style errors
    mock_managers['style'].get_style.side_effect = Exception("Style Error")
    main_window.on_style_changed("test_style")
    assert "Error" in main_window.status_label.text()
    
    # Test webcam errors
    mock_managers['webcam'].start.side_effect = Exception("Webcam Error")
    main_window.start_virtual_camera()
    assert "Error" in main_window.status_label.text()
    
    # Test settings errors
    mock_managers['settings'].save_settings.side_effect = Exception("Settings Error")
    main_window.save_settings()
    assert "Error" in main_window.status_label.text()

def test_gui_integration(main_window, qtbot):
    """Test integration between GUI components."""
    assert main_window is not None
    assert main_window.device_manager is not None
    assert main_window.style_tab_manager is not None
    assert main_window.parameter_controls is not None
    assert main_window.action_buttons is not None 