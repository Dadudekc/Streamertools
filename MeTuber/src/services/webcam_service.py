import logging
import threading
import time
import av
import cv2
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal
from typing import Optional, Dict, Any
from pyvirtualcam import Camera, PixelFormat

class WebcamService(QObject):
    """Service for managing webcam input and virtual camera output."""
    
    frame_ready = pyqtSignal(np.ndarray)
    error_signal = pyqtSignal(str)
    info_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        # Initialize state
        self._is_running = False
        self._container = None
        self._camera = None
        self._style_instance = None
        self._style_params = {}
        self._thread = None
        self._last_frame = None
        self._input_device = ""
        
    def start(self, device: str, style_instance: Any, style_params: Dict[str, Any]) -> bool:
        """Start the webcam service.
        
        Args:
            device (str): Device identifier
            style_instance: Style instance to apply
            style_params (dict): Style parameters
            
        Returns:
            bool: True if started successfully, False otherwise
        """
        try:
            if self._is_running:
                self.logger.warning("Webcam service is already running")
                return False
                
            # Open input device
            try:
                self._container = av.open(device, format="dshow")
                self._input_device = device
                self.logger.info(f"Opened input device: {device}")
                self.info_signal.emit(f"Opened input device: {device}")
            except av.AVError as e:
                error_msg = f"Error opening webcam: {e}"
                self.logger.error(error_msg)
                self.error_signal.emit(error_msg)
                return False
                
            # Open virtual camera
            try:
                self._camera = Camera(width=640, height=480, fps=30, fmt=PixelFormat.BGR)
                self.logger.info("Opened virtual camera")
                self.info_signal.emit("Opened virtual camera")
            except Exception as e:
                error_msg = f"Error opening virtual camera: {e}"
                self.logger.error(error_msg)
                self.error_signal.emit(error_msg)
                self._container.close()
                self._container = None
                return False
                
            # Store style information
            self._style_instance = style_instance
            self._style_params = style_params or {}
            
            # Start processing thread
            self._is_running = True
            self._thread = threading.Thread(target=self._process_frames)
            self._thread.start()
            
            self.logger.info("Webcam service started")
            self.info_signal.emit("Webcam service started")
            return True
            
        except Exception as e:
            error_msg = f"Error starting webcam service: {e}"
            self.logger.error(error_msg)
            self.error_signal.emit(error_msg)
            self.stop()
            return False
            
    def stop(self) -> None:
        """Stop the webcam service."""
        self._is_running = False
        
        # Wait for thread to finish
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)
            
        # Close resources
        if self._container:
            self._container.close()
            self._container = None
            
        if self._camera:
            self._camera.close()
            self._camera = None
            
        # Clear style information
        self._style_instance = None
        self._style_params = {}
        self._input_device = ""
        
        self.logger.info("Webcam service stopped")
        self.info_signal.emit("Webcam service stopped")
        
    def _process_frames(self) -> None:
        """Process frames from the input device."""
        try:
            while self._is_running:
                # Read frame from input
                for frame in self._container.decode(video=0):
                    if not self._is_running:
                        break
                        
                    # Convert to numpy array
                    frame_array = frame.to_ndarray(format="bgr24")
                    
                    # Apply style if available
                    if self._style_instance and self._style_params:
                        try:
                            frame_array = self._style_instance.apply(frame_array, self._style_params)
                            # Ensure BGR format
                            if len(frame_array.shape) == 2:
                                frame_array = cv2.cvtColor(frame_array, cv2.COLOR_GRAY2BGR)
                        except Exception as e:
                            self.logger.error(f"Error applying style: {e}")
                            self.error_signal.emit(f"Error applying style: {e}")
                            
                    # Save last frame
                    self._last_frame = frame_array.copy()
                    
                    # Emit frame
                    self.frame_ready.emit(frame_array)
                    
                    # Write to virtual camera
                    if self._camera:
                        try:
                            self._camera.send(frame_array)
                        except Exception as e:
                            self.logger.error(f"Error writing to virtual camera: {e}")
                            self.error_signal.emit(f"Error writing to virtual camera: {e}")
                            
        except Exception as e:
            error_msg = f"Error processing frames: {e}"
            self.logger.error(error_msg)
            self.error_signal.emit(error_msg)
        finally:
            self._is_running = False
            
    def update_parameters(self, params: Dict[str, Any]) -> None:
        """Update style parameters.
        
        Args:
            params (dict): New style parameters
        """
        self._style_params = params or {}
        
    def get_last_frame(self) -> Optional[np.ndarray]:
        """Get the last processed frame.
        
        Returns:
            numpy.ndarray: Last processed frame or None if no frame available
        """
        return self._last_frame
        
    def is_running(self) -> bool:
        """Check if the service is running.
        
        Returns:
            bool: True if running, False otherwise
        """
        return self._is_running 