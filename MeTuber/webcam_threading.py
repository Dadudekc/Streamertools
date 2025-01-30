# D:\MeTuber\MeTuber\webcam_threading.py

import av
import pyvirtualcam
import logging
from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import numpy as np


class WebcamThread(QThread):
    """
    A QThread that captures video frames using PyAV, applies the chosen style,
    and publishes them to a virtual camera with pyvirtualcam.
    """
    error_signal = pyqtSignal(str)
    info_signal = pyqtSignal(str)

    last_frame = None  # For snapshot feature

    def __init__(self, input_device, style_instance, style_params, log_level=logging.INFO):
        super().__init__()
        self.input_device = input_device
        self.style_instance = style_instance
        self.style_params = style_params
        self._is_running = True
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)
        # Prevent duplicate logs
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        # Attempt to import CameraError with fallback
        try:
            from pyvirtualcam import CameraError
            self.CameraError = CameraError
        except ImportError:
            try:
                from pyvirtualcam.errors import CameraError
                self.CameraError = CameraError
            except ImportError:
                self.CameraError = Exception  # Fallback to generic Exception

    def run(self):
        """
        Continuously decode frames from the specified device using PyAV,
        apply the chosen style, and send them to a virtual camera.
        """
        self.logger.info("WebcamThread started.")
        self.info_signal.emit("Webcam thread started.")

        container = None

        try:
            # 1. Open the device with PyAV
            try:
                container = av.open(self.input_device, format="dshow")
                self.logger.info(f"Opened input device: {self.input_device}")
                self.info_signal.emit(f"Opened input device: {self.input_device}")
            except av.AVError as e:
                error_msg = f"Error opening webcam with PyAV: {e}"
                self.logger.error(error_msg)
                self.error_signal.emit(error_msg)
                return

            # 2. Start a pyvirtualcam Camera
            try:
                # Fetch default camera properties or set custom ones
                # Here, using 640x480 at 30 FPS as an example
                with pyvirtualcam.Camera(width=640, height=480, fps=30, fmt=pyvirtualcam.PixelFormat.BGR) as cam:
                    self.logger.info(f"Opened virtual camera: {cam.device}")
                    self.info_signal.emit(f"Opened virtual camera: {cam.device}")
                    for frame in container.decode(video=0):
                        if not self._is_running:
                            self.logger.info("WebcamThread stopping as requested.")
                            self.info_signal.emit("Webcam thread stopping.")
                            break

                        try:
                            # Convert PyAV frame to NumPy array (BGR24)
                            img = frame.to_ndarray(format="bgr24")

                            # Apply the selected style
                            processed_frame = self.style_instance.apply(img, self.style_params)

                            # Ensure processed_frame is in BGR format
                            if len(processed_frame.shape) == 2:
                                processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_GRAY2BGR)

                            # Resize to match virtual camera resolution
                            resized_frame = cv2.resize(processed_frame, (cam.width, cam.height))

                            # Send frame to virtual camera
                            cam.send(resized_frame)
                            cam.sleep_until_next_frame()

                            # Save the last processed frame for snapshots
                            self.last_frame = resized_frame.copy()

                        except ValueError as ve:
                            error_msg = f"Parameter Error: {ve}"
                            self.logger.error(error_msg)
                            self.error_signal.emit(error_msg)
                            self.stop()
                            break

                        except Exception as e:
                            error_msg = f"Unexpected error during frame processing: {e}"
                            self.logger.error(error_msg)
                            self.error_signal.emit(error_msg)
                            self.stop()
                            break

            except self.CameraError as e:
                error_msg = f"Error initializing virtual camera: {e}"
                self.logger.error(error_msg)
                self.error_signal.emit(error_msg)
                return

        except Exception as e:
            # Catch-all for any other exceptions
            error_msg = f"Unexpected error in WebcamThread: {e}"
            self.logger.error(error_msg)
            self.error_signal.emit(error_msg)

        finally:
            # Ensure resources are released
            if container:
                container.close()
                self.logger.info("Input container closed.")
            self.logger.info("WebcamThread terminated.")
            self.info_signal.emit("Webcam thread terminated.")

    def update_params(self, new_params):
        """Update style parameters in real-time."""
        self.style_params = new_params
        self.logger.info("WebcamThread parameters updated.")
        self.info_signal.emit("Style parameters updated.")

    def stop(self):
        """Stop the webcam processing loop."""
        self._is_running = False
        self.wait()  # Ensure the thread has fully stopped before returning
        self.logger.info("WebcamThread has been stopped.")
        self.info_signal.emit("Webcam thread has been stopped.")
