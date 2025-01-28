# MeTuber\tests\test_webcam_threading.py

import unittest
from unittest.mock import patch, MagicMock
from webcam_threading import WebcamThread
from styles.effects.original import Original
from pyvirtualcam import PixelFormat


class TestWebcamThreading(unittest.TestCase):

    @patch('webcam_threading.av.open')  # Adjusted patch path
    @patch('webcam_threading.pyvirtualcam.Camera')  # Adjusted patch path
    def test_thread_initialization(self, mock_camera, mock_av_open):
        """Test if WebcamThread initializes correctly."""
        mock_av_instance = MagicMock()
        mock_av_open.return_value = mock_av_instance

        mock_cam_instance = MagicMock()
        mock_camera.return_value.__enter__.return_value = mock_cam_instance

        style = Original()
        params = {}

        thread = WebcamThread("video=TestDevice", style, params)
        thread.start()

        # Ensure av.open was called with the correct device
        mock_av_open.assert_called_with("video=TestDevice", format="dshow")

        # Ensure pyvirtualcam.Camera was initialized correctly
        mock_camera.assert_called_with(width=640, height=480, fps=30, fmt=PixelFormat.BGR)

        # Stop the thread
        thread.stop()

        # Assert the thread is no longer running
        self.assertFalse(thread._is_running)  # Correct attribute used
