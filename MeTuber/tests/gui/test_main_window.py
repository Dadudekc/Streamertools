import pytest
from unittest.mock import MagicMock, patch
import numpy as np
from PyQt5.QtWidgets import QApplication
from src.gui.main_window import MainWindow

@pytest.fixture
def mock_managers():
    """Create mock manager instances."""
    with patch('src.config.settings_manager.SettingsManager') as mock_settings, \
         patch('src.core.device_manager.DeviceManagerFactory') as mock_device_factory, \
         patch('src.core.style_manager.StyleManager') as mock_style, \
         patch('src.services.webcam_service.WebcamService') as mock_webcam:
        
        # Setup mock managers
        mock_settings.return_value = MagicMock()
        mock_device = MagicMock()
        mock_device_factory.create.return_value = mock_device
        mock_style.return_value = MagicMock()
        mock_webcam.return_value = MagicMock()
        
        yield {
            'settings': mock_settings.return_value,
            'device': mock_device,
            'style': mock_style.return_value,
            'webcam': mock_webcam.return_value
        }

@pytest.fixture
def main_window(qtbot, mock_managers):
    """Create a MainWindow instance."""
    window = MainWindow()
    window.device_manager = mock_managers['device']
    window.style_manager = mock_managers['style']
    window.webcam_service = mock_managers['webcam']
    window.settings_manager = mock_managers['settings']
    qtbot.addWidget(window)
    return window

def test_main_window_initialization(main_window):
    """Test main window initialization."""
    assert main_window is not None
    assert main_window.device_manager is not None
    assert main_window.style_manager is not None
    assert main_window.webcam_service is not None
    assert main_window.settings_manager is not None

def test_main_window_load_settings(main_window, mock_managers):
    """Test loading settings."""
    mock_managers['settings'].get_setting.side_effect = lambda key: {
        "input_device": "test_device",
        "style": "test_style",
        "parameters": {"param1": 50}
    }.get(key, None)
    
    main_window.load_settings()
    mock_managers['settings'].get_setting.assert_called()

def test_main_window_save_settings(main_window, mock_managers):
    """Test saving settings."""
    main_window.save_settings()
    mock_managers['settings'].set_setting.assert_called()
    mock_managers['settings'].save_settings.assert_called()

def test_main_window_start_virtual_camera(main_window, mock_managers):
    """Test starting virtual camera."""
    mock_managers['device'].validate_device.return_value = True
    mock_managers['webcam'].start.return_value = True
    
    assert main_window.start_virtual_camera()
    assert main_window.status_label.text() == "Status: Running"

def test_main_window_stop_virtual_camera(main_window, mock_managers):
    """Test stopping virtual camera."""
    main_window.stop_virtual_camera()
    mock_managers['webcam'].stop.assert_called_once()
    assert main_window.status_label.text() == "Status: Idle"

def test_main_window_take_snapshot(main_window, mock_managers):
    """Test taking snapshot."""
    mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    mock_managers['webcam'].get_last_frame.return_value = mock_frame
    
    with patch('cv2.imwrite') as mock_imwrite:
        main_window.take_snapshot()
        mock_imwrite.assert_called_once()

def test_main_window_update_preview(main_window):
    """Test updating preview."""
    mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    main_window.update_preview(mock_frame)
    assert main_window.preview_label.pixmap() is not None

def test_main_window_display_error(main_window):
    """Test displaying error message."""
    main_window.display_error("Test Error")
    assert main_window.status_label.text() == "Error: Test Error"

def test_main_window_display_info(main_window):
    """Test displaying info message."""
    main_window.display_info("Test Info")
    assert main_window.status_label.text() == "Status: Test Info"

def test_main_window_close_event(main_window, mock_managers):
    """Test close event handling."""
    main_window.close()
    mock_managers['webcam'].stop.assert_called_once()
    mock_managers['settings'].save_settings.assert_called_once() 