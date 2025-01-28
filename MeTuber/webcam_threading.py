# webcam_filter_pyqt5\webcam_threading.py

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

    def __init__(self, input_device, style_instance, style_params):
        super().__init__()
        self.input_device = input_device
        self.style_instance = style_instance
        self.style_params = style_params
        self._is_running = True

    def run(self):
        """
        Continuously decode frames from the specified device using PyAV,
        apply the chosen style, and send them to a virtual camera.
        """
        logging.info("WebcamThread started.")
        self.info_signal.emit("Webcam thread started.")

        container = None
        camera = None

        try:
            # 1. Open the device with PyAV
            try:
                container = av.open(self.input_device, format="dshow")
                logging.info(f"Opened input device: {self.input_device}")
                self.info_signal.emit(f"Opened input device: {self.input_device}")
            except av.AVError as e:
                error_msg = f"Error opening webcam with PyAV: {e}"
                logging.error(error_msg)
                self.error_signal.emit(error_msg)
                return

            # 2. Start a pyvirtualcam Camera
            try:
                camera = pyvirtualcam.Camera(width=640, height=480, fps=30, fmt=pyvirtualcam.PixelFormat.BGR)
                logging.info(f"Virtual camera started: {camera.device}")
                self.info_signal.emit(f"Virtual camera started: {camera.device}")
            except pyvirtualcam.CameraError as e:
                error_msg = f"Error initializing virtual camera: {e}"
                logging.error(error_msg)
                self.error_signal.emit(error_msg)
                return

            # 3. Process frames
            for frame in container.decode(video=0):
                if not self._is_running:
                    logging.info("WebcamThread stopping as requested.")
                    self.info_signal.emit("Webcam thread stopping.")
                    break

                try:
                    # Convert PyAV frame to NumPy array (BGR24)
                    img = frame.to_ndarray(format="bgr24")

                    # Apply the selected style (with current style parameters)
                    styled_frame = self.style_instance.apply(img, self.style_params)

                    # Convert single-channel frames to BGR if needed
                    if len(styled_frame.shape) == 2:
                        styled_frame = cv2.cvtColor(styled_frame, cv2.COLOR_GRAY2BGR)

                    # Resize to match virtual camera resolution
                    resized_frame = cv2.resize(styled_frame, (camera.width, camera.height))

                    # Send frame to virtual camera
                    camera.send(resized_frame)
                    camera.sleep_until_next_frame()

                    # Save the last processed frame for snapshots
                    self.last_frame = resized_frame.copy()

                except ValueError as ve:
                    error_msg = f"Parameter Error: {ve}"
                    logging.error(error_msg)
                    self.error_signal.emit(error_msg)
                    self.stop()
                    break

                except Exception as e:
                    error_msg = f"Unexpected error during frame processing: {e}"
                    logging.error(error_msg)
                    self.error_signal.emit(error_msg)
                    self.stop()
                    break

        except Exception as e:
            # Catch-all for any other exceptions
            error_msg = f"Unexpected error in WebcamThread: {e}"
            logging.error(error_msg)
            self.error_signal.emit(error_msg)

        finally:
            # Ensure resources are released
            if container:
                container.close()
                logging.info("Input container closed.")
            if camera:
                camera.close()
                logging.info("Virtual camera closed.")

            logging.info("WebcamThread terminated.")
            self.info_signal.emit("Webcam thread terminated.")

    def update_params(self, new_params):
        """Update style parameters in real-time."""
        self.style_params = new_params
        logging.info("WebcamThread parameters updated.")
        self.info_signal.emit("Style parameters updated.")

    def stop(self):
        """Stop the webcam processing loop."""
        self._is_running = False
        self.wait()  # Ensure the thread has fully stopped before returning
        logging.info("WebcamThread has been stopped.")
        self.info_signal.emit("Webcam thread has been stopped.")
