import logging
from typing import Optional, Dict, Any
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QProgressBar, QGroupBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QSize
from PyQt5.QtGui import QPixmap, QImage, QPainter, QFont, QColor

class PreviewArea(QWidget):
    """Real-time preview area for webcam feed with style effects."""
    
    # Signals
    preview_clicked = pyqtSignal()  # When preview area is clicked
    snapshot_requested = pyqtSignal()  # When snapshot is requested
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        
        # Preview state
        self.current_frame = None
        self.is_playing = False
        self.fps = 0
        self.frame_count = 0
        self.last_fps_update = 0
        
        # Performance metrics
        self.processing_time = 0
        self.memory_usage = 0
        self.cpu_usage = 0
        
        # UI components
        self.preview_label = None
        self.status_label = None
        self.fps_label = None
        self.performance_bar = None
        self.snapshot_button = None
        
        # Timer for FPS calculation
        self.fps_timer = QTimer()
        self.fps_timer.timeout.connect(self._update_fps)
        self.fps_timer.start(1000)  # Update every second
        
        # Initialize UI
        self.init_ui()
        
    def init_ui(self) -> None:
        """Initialize the preview area UI."""
        try:
            layout = QVBoxLayout()
            self.setLayout(layout)
            
            # Title
            title = QLabel("📹 Live Preview")
            title.setFont(QFont("Segoe UI", 14, QFont.Bold))
            title.setAlignment(Qt.AlignCenter)
            layout.addWidget(title)
            
            # Preview frame
            self.preview_label = QLabel()
            self.preview_label.setAlignment(Qt.AlignCenter)
            self.preview_label.setMinimumSize(640, 480)
            self.preview_label.setStyleSheet("""
                QLabel {
                    background-color: #000000;
                    border: 2px solid #404040;
                    border-radius: 8px;
                    padding: 8px;
                }
                QLabel:hover {
                    border-color: #007acc;
                }
            """)
            self.preview_label.setCursor(Qt.PointingHandCursor)
            self.preview_label.mousePressEvent = self._on_preview_clicked
            layout.addWidget(self.preview_label)
            
            # Status and controls
            controls_layout = QHBoxLayout()
            
            # Status indicators
            status_group = QGroupBox("Status")
            status_layout = QVBoxLayout()
            status_group.setLayout(status_layout)
            
            self.status_label = QLabel("⏸️ Stopped")
            self.status_label.setStyleSheet("color: #cccccc; font-weight: bold;")
            status_layout.addWidget(self.status_label)
            
            self.fps_label = QLabel("FPS: 0")
            self.fps_label.setStyleSheet("color: #4ec9b0;")
            status_layout.addWidget(self.fps_label)
            
            controls_layout.addWidget(status_group)
            
            # Performance metrics
            perf_group = QGroupBox("Performance")
            perf_layout = QVBoxLayout()
            perf_group.setLayout(perf_layout)
            
            # CPU usage
            cpu_label = QLabel("CPU: 0%")
            cpu_label.setStyleSheet("color: #ff9800;")
            perf_layout.addWidget(cpu_label)
            
            # Memory usage
            memory_label = QLabel("Memory: 0 MB")
            memory_label.setStyleSheet("color: #f44336;")
            perf_layout.addWidget(memory_label)
            
            # Processing time
            processing_label = QLabel("Processing: 0ms")
            processing_label.setStyleSheet("color: #4caf50;")
            perf_layout.addWidget(processing_label)
            
            controls_layout.addWidget(perf_group)
            
            # Snapshot button
            self.snapshot_button = QPushButton("📸 Take Snapshot")
            self.snapshot_button.setEnabled(False)
            self.snapshot_button.clicked.connect(self._on_snapshot_clicked)
            controls_layout.addWidget(self.snapshot_button)
            
            layout.addLayout(controls_layout)
            
            # Performance bar
            self.performance_bar = QProgressBar()
            self.performance_bar.setRange(0, 100)
            self.performance_bar.setValue(0)
            self.performance_bar.setFormat("Performance: %p%")
            self.performance_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #404040;
                    border-radius: 4px;
                    text-align: center;
                    background-color: #1a1a1a;
                }
                QProgressBar::chunk {
                    background-color: #007acc;
                    border-radius: 3px;
                }
            """)
            layout.addWidget(self.performance_bar)
            
            # Set initial preview
            self._set_placeholder_preview()
            
            self.logger.info("Preview area UI initialized")
            
        except Exception as e:
            self.logger.error(f"Error initializing preview area UI: {e}")
    
    def _set_placeholder_preview(self) -> None:
        """Set a placeholder preview when no camera is active."""
        try:
            # Create a placeholder image
            placeholder = QPixmap(640, 480)
            placeholder.fill(QColor(0, 0, 0))
            
            # Draw placeholder text
            painter = QPainter(placeholder)
            painter.setPen(QColor(255, 255, 255))
            painter.setFont(QFont("Segoe UI", 16))
            
            # Draw camera icon and text
            text = "📹\nClick to Start Camera"
            painter.drawText(placeholder.rect(), Qt.AlignCenter, text)
            painter.end()
            
            self.preview_label.setPixmap(placeholder)
            
        except Exception as e:
            self.logger.error(f"Error setting placeholder preview: {e}")
    
    def update_preview(self, frame) -> None:
        """Update the preview with a new frame."""
        try:
            if frame is None:
                return
            
            self.current_frame = frame
            self.frame_count += 1
            
            # Convert frame to QPixmap
            if hasattr(frame, 'shape'):
                # NumPy array
                height, width, channel = frame.shape
                bytes_per_line = 3 * width
                
                # Convert BGR to RGB
                rgb_frame = frame[:, :, ::-1]
                
                q_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)
            else:
                # Assume it's already a QPixmap or QImage
                if isinstance(frame, QPixmap):
                    pixmap = frame
                elif isinstance(frame, QImage):
                    pixmap = QPixmap.fromImage(frame)
                else:
                    self.logger.warning(f"Unknown frame type: {type(frame)}")
                    return
            
            # Scale pixmap to fit preview area while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(
                self.preview_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            self.preview_label.setPixmap(scaled_pixmap)
            
        except Exception as e:
            self.logger.error(f"Error updating preview: {e}")
    
    def set_playing_state(self, is_playing: bool) -> None:
        """Set the playing state of the preview."""
        try:
            self.is_playing = is_playing
            
            if is_playing:
                self.status_label.setText("▶️ Playing")
                self.status_label.setStyleSheet("color: #4caf50; font-weight: bold;")
                self.snapshot_button.setEnabled(True)
            else:
                self.status_label.setText("⏸️ Stopped")
                self.status_label.setStyleSheet("color: #cccccc; font-weight: bold;")
                self._set_placeholder_preview()
            
        except Exception as e:
            self.logger.error(f"Error setting playing state: {e}")
    
    def update_performance_metrics(self, cpu: float, memory: float, processing_time: float) -> None:
        """Update performance metrics display."""
        try:
            self.cpu_usage = cpu
            self.memory_usage = memory
            self.processing_time = processing_time
            
            # Update performance bar (average of CPU and memory usage)
            performance_score = min(100, (cpu + memory) / 2)
            self.performance_bar.setValue(int(performance_score))
            
            # Update performance bar color based on score
            if performance_score < 50:
                color = "#4caf50"  # Green
            elif performance_score < 80:
                color = "#ff9800"  # Orange
            else:
                color = "#f44336"  # Red
            
            self.performance_bar.setStyleSheet(f"""
                QProgressBar {{
                    border: 1px solid #404040;
                    border-radius: 4px;
                    text-align: center;
                    background-color: #1a1a1a;
                }}
                QProgressBar::chunk {{
                    background-color: {color};
                    border-radius: 3px;
                }}
            """)
            
        except Exception as e:
            self.logger.error(f"Error updating performance metrics: {e}")
    
    def _update_fps(self) -> None:
        """Update FPS display."""
        try:
            self.fps = self.frame_count
            self.fps_label.setText(f"FPS: {self.fps}")
            self.frame_count = 0
            
        except Exception as e:
            self.logger.error(f"Error updating FPS: {e}")
    
    def _on_preview_clicked(self, event) -> None:
        """Handle preview area click."""
        try:
            if not self.is_playing:
                self.preview_clicked.emit()
            
        except Exception as e:
            self.logger.error(f"Error handling preview click: {e}")
    
    def _on_snapshot_clicked(self) -> None:
        """Handle snapshot button click."""
        try:
            self.snapshot_requested.emit()
            
        except Exception as e:
            self.logger.error(f"Error handling snapshot click: {e}")
    
    def get_preview_size(self) -> QSize:
        """Get the current preview size."""
        return self.preview_label.size()
    
    def set_preview_size(self, width: int, height: int) -> None:
        """Set the preview size."""
        try:
            self.preview_label.setMinimumSize(width, height)
            
        except Exception as e:
            self.logger.error(f"Error setting preview size: {e}")
    
    def show_error(self, message: str) -> None:
        """Show an error message in the preview area."""
        try:
            self.status_label.setText(f"❌ {message}")
            self.status_label.setStyleSheet("color: #f44336; font-weight: bold;")
            
        except Exception as e:
            self.logger.error(f"Error showing error message: {e}")
    
    def show_info(self, message: str) -> None:
        """Show an info message in the preview area."""
        try:
            self.status_label.setText(f"ℹ️ {message}")
            self.status_label.setStyleSheet("color: #007acc; font-weight: bold;")
            
        except Exception as e:
            self.logger.error(f"Error showing info message: {e}")
    
    def clear_messages(self) -> None:
        """Clear status messages."""
        try:
            if self.is_playing:
                self.status_label.setText("▶️ Playing")
                self.status_label.setStyleSheet("color: #4caf50; font-weight: bold;")
            else:
                self.status_label.setText("⏸️ Stopped")
                self.status_label.setStyleSheet("color: #cccccc; font-weight: bold;")
            
        except Exception as e:
            self.logger.error(f"Error clearing messages: {e}") 