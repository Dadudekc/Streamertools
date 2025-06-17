# MeTuber\tests\test_webcam_threading.py

import pytest
from unittest.mock import MagicMock, patch
from styles.effects.original import Original
from pyvirtualcam import PixelFormat
from webcam_threading import WebcamThread

@pytest.mark.usefixtures("qapp")
class TestWebcamThreading:
    """Test cases for WebcamThread class."""

    @pytest.fixture
    def webcam_thread(self, request):
        """Fixture to manage WebcamThread lifecycle."""
        thread = None
        def cleanup():
            if thread is not None and thread.is_alive():
                thread.stop()
                thread.join(timeout=5)
        request.addfinalizer(cleanup)
        return thread

    @pytest.fixture(autouse=True)
    def setup_test(self, qtbot):
        """Setup test environment."""
        self.qtbot = qtbot
        yield

    @patch('webcam_threading.av.open')
    @patch('webcam_threading.pyvirtualcam.Camera')
    def test_thread_initialization(self, mock_camera, mock_av_open, webcam_thread, qtbot):
        """Test if WebcamThread initializes correctly."""
        mock_av_instance = MagicMock()
        mock_av_open.return_value = mock_av_instance

        mock_cam_instance = MagicMock()
        mock_camera.return_value.__enter__.return_value = mock_cam_instance

        style = Original()
        params = {}

        thread = WebcamThread("video=TestDevice", style, params)
        webcam_thread = thread  # Assign to fixture for cleanup
        
        with qtbot.waitSignal(thread.started, timeout=5000):
            thread.start()

        # Ensure av.open was called with the correct device
        mock_av_open.assert_called_with("video=TestDevice", format="dshow")

        # Ensure pyvirtualcam.Camera was initialized correctly
        mock_camera.assert_called_with(width=640, height=480, fps=30, fmt=PixelFormat.BGR)

        # Stop the thread
        with qtbot.waitSignal(thread.finished, timeout=5000):
            thread.stop()
            thread.wait()

        assert not thread._is_running  # Using pytest style assertions
