import pytest
from unittest.mock import MagicMock, patch
from PyQt5.QtCore import Qt

from src.gui.v2_main_window import V2MainWindow


@pytest.fixture
def mock_managers():
    """Create mock manager instances for V2MainWindow."""
    with patch('src.gui.v2_main_window.SettingsManager') as mock_settings, \
         patch('src.gui.v2_main_window.DeviceManagerFactory') as mock_device_factory, \
         patch('src.gui.v2_main_window.StyleManager') as mock_style, \
         patch('src.gui.v2_main_window.WebcamService') as mock_webcam:

        mock_settings_instance = MagicMock()
        mock_settings.return_value = mock_settings_instance
        mock_device = MagicMock()
        mock_device_factory.create.return_value = mock_device
        mock_style.return_value = MagicMock()
        mock_webcam_instance = MagicMock()
        mock_webcam.return_value = mock_webcam_instance

        yield {
            'settings': mock_settings_instance,
            'device': mock_device,
            'style': mock_style.return_value,
            'webcam': mock_webcam_instance,
        }


@pytest.fixture
def v2_main_window(qtbot, mock_managers):
    """Create a V2MainWindow instance for testing."""
    window = V2MainWindow()
    qtbot.addWidget(window)
    return window


def test_stop_camera_via_ui_disables_snapshot(v2_main_window, qtbot):
    """Stopping the camera via the UI disables the snapshot button."""
    window = v2_main_window
    # Simulate running state
    window.action_buttons.snapshot_button.setEnabled(True)
    window.action_buttons.stop_button.setEnabled(True)

    qtbot.mouseClick(window.action_buttons.stop_button, Qt.LeftButton)

    assert not window.action_buttons.snapshot_button.isEnabled()


def test_stop_camera_programmatically_disables_snapshot(v2_main_window):
    """Stopping the camera programmatically disables the snapshot button."""
    window = v2_main_window
    window.action_buttons.snapshot_button.setEnabled(True)
    window.action_buttons.stop_button.setEnabled(True)

    window._stop_camera()

    assert not window.action_buttons.snapshot_button.isEnabled()
