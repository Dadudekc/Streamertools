# D:\MeTuber\MeTuber\webcam_threading.py

import av
import pyvirtualcam
import logging
from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import numpy as np
import os
import traceback
import time
import queue
from collections import deque

DEBUG_MODE = os.environ.get("METUBER_DEBUG", "0") == "1"


class WebcamThread(QThread):
    """
    A QThread that captures video frames using PyAV, applies the chosen style,
    and publishes them to a virtual camera with pyvirtualcam.
    """
    error_signal = pyqtSignal(str, object)  # message, exception
    info_signal = pyqtSignal(str)

    last_frame = None  # For snapshot feature

    def __init__(self, input_device, style_instance, style_params):
        super().__init__()
        self.input_device = input_device
        self.style_instance = style_instance
        self.style_params = style_params
        self.running = False
        self.last_frame = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
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

        # Buffer management settings
        self.max_fps = 30  # Limit frame rate
        self.frame_skip = 0  # Skip every Nth frame (0 = no skip)
        self.frame_count = 0
        self.last_frame_time = 0
        
        # Frame queue to prevent buffer buildup
        self.frame_queue = deque(maxlen=5)  # Only keep 5 frames max
        
        # PyAV input options to reduce buffer size aggressively
        self.input_options = {
            'rtbufsize': '256k',  # Very small buffer (was 1024k)
            'fflags': 'nobuffer+discardcorrupt',  # Disable buffering + discard corrupt frames
            'flags': 'low_delay',  # Low delay mode
            'framedrop': '1',      # Drop frames if needed
            'sync': 'ext',         # External sync
            'probesize': '32',     # Minimal probe size
            'analyzeduration': '0' # No analysis delay
        }

    def run(self):
        """
        Continuously decode frames from the specified device using PyAV,
        apply the chosen style, and send them to a virtual camera.
        """
        self.logger.info("WebcamThread started.")
        self.info_signal.emit("Webcam thread started.")
        
        try:
            # Open input stream with aggressive buffer management options
            input_stream = av.open(
                self.input_device,
                options=self.input_options,
                timeout=0.1  # Very short timeout (was 1.0)
            )
            
            # Get video stream
            video_stream = input_stream.streams.video[0]
            video_stream.thread_type = 'AUTO'  # Use threading for decoding
            
            # Set up virtual camera with lower FPS
            target_fps = min(self.max_fps, 15)  # Cap at 15 FPS to reduce load
            with pyvirtualcam.Camera(width=video_stream.width, height=video_stream.height, fps=target_fps) as cam:
                self.logger.info(f"Virtual camera initialized: {video_stream.width}x{video_stream.height} @ {target_fps}fps")
                self.info_signal.emit(f"Virtual camera ready: {video_stream.width}x{video_stream.height}")
                
                frame_interval = 1.0 / target_fps
                frames_processed = 0
                frames_dropped = 0
                last_stats_time = time.time()
                
                for frame in input_stream.decode(video=0):
                    if not self.running:
                        break
                    
                    # Aggressive frame rate limiting
                    current_time = time.time()
                    if current_time - self.last_frame_time < frame_interval:
                        frames_dropped += 1
                        continue
                    
                    # Frame skipping
                    self.frame_count += 1
                    if self.frame_skip > 0 and self.frame_count % (self.frame_skip + 1) != 0:
                        frames_dropped += 1
                        continue
                    
                    # Queue management - drop old frames if queue is full
                    if len(self.frame_queue) >= 3:  # Keep queue small
                        try:
                            self.frame_queue.popleft()  # Drop oldest frame
                            frames_dropped += 1
                        except IndexError:
                            pass
                    
                    try:
                        # Convert frame to numpy array
                        frame_array = frame.to_ndarray(format='bgr24')
                        
                        # Add to queue
                        self.frame_queue.append(frame_array)
                        
                        # Apply style
                        if self.style_instance:
                            processed_frame = self.style_instance.apply(frame_array, self.style_params)
                        else:
                            processed_frame = frame_array
                        
                        # Send to virtual camera
                        cam.send(processed_frame)
                        cam.sleep_until_next_frame()
                        
                        # Store last frame for snapshot
                        self.last_frame = processed_frame.copy()
                        self.last_frame_time = current_time
                        frames_processed += 1
                        
                        # Log stats every 5 seconds
                        if current_time - last_stats_time > 5.0:
                            self.logger.info(f"Buffer stats: {frames_processed} processed, {frames_dropped} dropped")
                            frames_processed = 0
                            frames_dropped = 0
                            last_stats_time = current_time
                        
                    except Exception as frame_error:
                        self.logger.warning(f"Frame processing error: {frame_error}")
                        frames_dropped += 1
                        # Continue processing other frames
                        continue
                        
        except av.EOFError:
            self.logger.info("End of video stream reached.")
            self.info_signal.emit("Video stream ended.")
        except av.error.EOFError:
            self.logger.info("End of video stream reached.")
            self.info_signal.emit("Video stream ended.")
        except Exception as e:
            error_msg = f"Unexpected error in WebcamThread: {e}"
            self.logger.error(error_msg, exc_info=True)
            if DEBUG_MODE:
                tb = traceback.format_exc()
                self.error_signal.emit(f"{error_msg}\n\nTraceback:\n{tb}", e)
            else:
                self.error_signal.emit(error_msg, e)
        finally:
            try:
                input_stream.close()
            except:
                pass
            self.logger.info("WebcamThread stopped.")

    def update_params(self, new_params):
        """Update style parameters and buffer settings."""
        self.style_params = new_params
        # Allow frame rate control via parameters
        if 'max_fps' in new_params:
            self.max_fps = max(1, min(60, new_params['max_fps']))
        if 'frame_skip' in new_params:
            self.frame_skip = max(0, min(10, new_params['frame_skip']))

    def stop(self):
        """Stop the thread."""
        self.running = False
        self.wait()  # Wait for thread to finish
