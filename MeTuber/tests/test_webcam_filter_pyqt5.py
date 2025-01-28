
import numpy as np
import os
import subprocess
import json
import unittest
from unittest.mock import patch, MagicMock, mock_open
from webcam_filter_pyqt5 import (
    load_settings,
    save_settings,
    list_devices,
    load_styles,
    WebcamThread,
    WebcamApp,
)
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication, QPushButton, QMessageBox

app = QApplication([])  # Required for testing PyQt5

CONFIG_FILE = "config.json"

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.default_settings = {
            "input_device": "video=C270 HD WEBCAM",
            "style": "Original",
            "parameters": {}
        }

    @patch("webcam_filter_pyqt5.open", new_callable=mock_open, read_data=json.dumps({"style": "CustomStyle"}))
    @patch("webcam_filter_pyqt5.os.path.exists", return_value=True)
    def test_load_settings_with_file(self, mock_exists, mock_open_file):
        settings = load_settings()
        self.assertEqual(settings["style"], "CustomStyle")

    @patch('json.dump')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_settings(self, mock_open, mock_json_dump):
        settings = {"key": "value"}
        save_settings(settings)
        mock_open.assert_called_once_with(CONFIG_FILE, "w")
        mock_json_dump.assert_called_once_with(settings, mock_open.return_value, indent=4)

    @patch("webcam_filter_pyqt5.os.path.exists", return_value=False)
    def test_load_settings_without_file(self, mock_exists):
        settings = load_settings()
        self.assertEqual(settings, self.default_settings)

    @patch('subprocess.check_output')
    def test_list_devices(self, mock_check_output):
        mock_check_output.return_value = b"""
            [dshow @ 000001C3E8C48040] DirectShow video devices (some may be both video and audio devices)
            [dshow @ 000001C3E8C48040]     "C270 HD WEBCAM"
            [dshow @ 000001C3E8C48040]     "OBS Virtual Camera"
        """
        devices = list_devices()
        print("Parsed Devices: ", devices)  # Debugging step
        self.assertIn("video=C270 HD WEBCAM", devices)
        self.assertIn("video=OBS Virtual Camera", devices)

    @patch("webcam_filter_pyqt5.subprocess.check_output", side_effect=subprocess.CalledProcessError(1, "ffmpeg"))
    def test_list_devices_error(self, mock_check_output):
        devices = list_devices()
        self.assertEqual(devices, [])

class TestStyleLoading(unittest.TestCase):
    @patch('pkgutil.walk_packages', return_value=[])
    @patch('importlib.import_module')
    def test_load_styles_empty(self, mock_import_module, mock_walk_packages):
        # Mock the __path__ attribute for the styles package
        mock_package = MagicMock()
        mock_package.__path__ = ["mock_path"]
        mock_import_module.return_value = mock_package

        styles, categories = load_styles()
        self.assertEqual(styles, {})
        self.assertEqual(categories, {})

class TestWebcamThread(unittest.TestCase):
    def setUp(self):
        self.dummy_style = MagicMock()
        self.dummy_style.apply = MagicMock(side_effect=lambda img, params: img)
        self.params = {"dummy_param": 0}
        self.input_device = "video=C270 HD WEBCAM"
        self.thread = WebcamThread(self.input_device, self.dummy_style, self.params)

    @patch('av.open')
    @patch('pyvirtualcam.Camera')
    def test_webcam_thread_run(self, mock_camera, mock_av_open):
        # Mock the Camera and AV objects
        mock_camera_instance = MagicMock()
        mock_camera.return_value.__enter__.return_value = mock_camera_instance
        mock_camera_instance.width = 640  # Mock camera resolution
        mock_camera_instance.height = 480
        mock_frame = MagicMock(to_ndarray=MagicMock(return_value=np.zeros((480, 640, 3), dtype=np.uint8)))
        mock_av_open.return_value.decode.return_value = [mock_frame]

        # Mock the style's apply method
        mock_style = MagicMock(apply=MagicMock(return_value=np.zeros((480, 640, 3))))

        # Initialize the thread
        thread = WebcamThread("mock_device", mock_style, {})
        thread._is_running = True

        # Simulate the thread's run method
        with patch.object(thread, 'stop', side_effect=lambda: setattr(thread, '_is_running', False)):
            print("Starting thread run...")
            thread.run()
            print("Thread run completed.")

        # Debugging: Print calls to `apply` and `send`
        print("Mock Style Apply Calls: ", mock_style.apply.call_args_list)
        print("Mock Camera Send Calls: ", mock_camera_instance.send.call_args_list)

        # Verify the `apply` method was called
        mock_style.apply.assert_called()
        # Verify the `send` method was called
        mock_camera_instance.send.assert_called_once()

class TestWebcamApp(unittest.TestCase):
    def setUp(self):
        self.app = WebcamApp()

    @patch('gui_components.parameter_controls.ParameterControls.update_parameters')
    def test_update_parameter_controls(self, mock_update_parameters):
        app = WebcamApp()
        app.current_style = MagicMock(parameters=[{"name": "mock_param"}])
        app.current_style_params = {"mock_param": 42}

        # Reset mock call count before explicitly calling the method
        mock_update_parameters.reset_mock()
        app.update_parameter_controls()

        # Assert single call
        mock_update_parameters.assert_called_once_with(
            app.current_style.parameters,
            app.current_style_params,
            app.on_param_changed
        )

    @patch('PyQt5.QtWidgets.QMessageBox.warning')
    @patch('PyQt5.QtWidgets.QComboBox.currentText', return_value="")
    def test_start_virtual_camera_no_device(self, mock_combo, mock_warning):
        app = WebcamApp()
        app.start_virtual_camera()
        mock_warning.assert_called_once_with(app, "Input Device Error", "Please specify a valid input device.")

    def test_start_virtual_camera_no_style(self):
        self.app.style_tab_manager.get_current_style = MagicMock(return_value=None)
        with patch.object(QMessageBox, "warning") as mock_warning:
            self.app.start_virtual_camera()
            mock_warning.assert_called_once_with(self.app, "Style Selection Error", "Please select a style.")

    def test_take_snapshot_no_frame(self):
        self.app.thread = None
        with patch.object(QMessageBox, "information") as mock_info:
            self.app.take_snapshot()
            mock_info.assert_called_once_with(self.app, "Snapshot", "No frame available to save.")

if __name__ == "__main__":
    unittest.main()
