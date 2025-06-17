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
        # Detect PyAV AVError exception class if available
        try:
            self.AVError = av.AVError
        except AttributeError:
            self.AVError = Exception

    def run(self):
        """
        Continuously decode frames from the specified device using PyAV,
        apply the chosen style, and send them to a virtual camera.
        """
        self.logger.info("WebcamThread started.")
        self.info_signal.emit("Webcam thread started.")

        container = None
        cap = None
        use_opencv = False

        try:
            # Attempt PyAV backend first
            try:
                container = av.open(self.input_device, format="dshow")
                self.logger.info(f"Using PyAV backend: {self.input_device}")
                self.info_signal.emit(f"Using PyAV backend: {self.input_device}")
            except self.AVError as e:
                self.logger.warning(f"PyAV failed ({e}), falling back to OpenCV capture.")
                self.info_signal.emit("Falling back to OpenCV capture.")
                use_opencv = True

            if not use_opencv:
                # PyAV + pyvirtualcam loop
                try:
                    with pyvirtualcam.Camera(width=640, height=480, fps=30, fmt=pyvirtualcam.PixelFormat.BGR) as cam:
                        self.logger.info(f"Opened virtual camera: {cam.device}")
                        self.info_signal.emit(f"Virtual camera: {cam.device}")
                        for frame in container.decode(video=0):
                            if not self._is_running:
                                break
                            img = frame.to_ndarray(format="bgr24")
                            processed = self.style_instance.apply(img, self.style_params)
                            if processed.ndim == 2:
                                processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
                            resized = cv2.resize(processed, (cam.width, cam.height))
                            cam.send(resized)
                            cam.sleep_until_next_frame()
                            self.last_frame = resized.copy()
                except self.CameraError as e:
                    error_msg = f"Virtual camera error: {e}"
                    self.logger.error(error_msg)
                    self.error_signal.emit(error_msg)
                    return
            else:
                # Fallback: OpenCV VideoCapture + pyvirtualcam
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    error_msg = "OpenCV fallback failed to open capture device."
                    self.logger.error(error_msg)
                    self.error_signal.emit(error_msg)
                    return
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = cap.get(cv2.CAP_PROP_FPS) or 30
                with pyvirtualcam.Camera(width=width, height=height, fps=fps, fmt=pyvirtualcam.PixelFormat.BGR) as cam:
                    self.logger.info("Using OpenCV fallback backend.")
                    self.info_signal.emit("OpenCV fallback active.")
                    while self._is_running:
                        ret, frame = cap.read()
                        if not ret:
                            break
                        processed = self.style_instance.apply(frame, self.style_params)
                        if processed.ndim == 2:
                            processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
                        resized = cv2.resize(processed, (cam.width, cam.height))
                        cam.send(resized)
                        cam.sleep_until_next_frame()
                        self.last_frame = resized.copy()
                cap.release()

        except Exception as e:
            # Catch-all for any other exceptions
            error_msg = f"Unexpected error in WebcamThread: {e}"
            self.logger.error(error_msg)
            self.error_signal.emit(error_msg)

        finally:
            # Ensure resources are released
            if container:
                container.close()
            if cap:
                cap.release()
            self.logger.info("WebcamThread terminated.")
            self.info_signal.emit("Webcam thread terminated.")

    def update_params(self, new_params):
        """Update style parameters in real-time."""
        self.style_params = new_params
        self.logger.info("WebcamThread parameters updated.")
        self.info_signal.emit("Style parameters updated.")

    def stop(self):
        """Signal the webcam processing loop to stop without blocking the caller."""
        self._is_running = False
        # Do not block the UI thread here; allow run() to exit and perform cleanup
        self.logger.info("WebcamThread stop requested; exiting loop soon.")
