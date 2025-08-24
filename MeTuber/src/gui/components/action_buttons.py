import logging
from typing import Optional, Callable
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSignal

class ActionButtons(QWidget):
    """Widget containing action buttons for controlling the webcam and taking snapshots."""
    
    start_camera = pyqtSignal()
    stop_camera = pyqtSignal()
    take_snapshot = pyqtSignal()
    
    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize the action buttons widget.
        
        Args:
            parent: Optional parent widget
        """
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self._init_ui()
        
    def _init_ui(self) -> None:
        """Initialize the user interface with action buttons."""
        try:
            layout = QHBoxLayout()
            
            # Create buttons
            self.start_button = QPushButton("Start Camera")
            self.stop_button = QPushButton("Stop Camera")
            self.snapshot_button = QPushButton("Take Snapshot")
            
            # Set initial button states
            self.stop_button.setEnabled(False)
            self.snapshot_button.setEnabled(False)
            
            # Connect signals
            self.start_button.clicked.connect(self._on_start_clicked)
            self.stop_button.clicked.connect(self._on_stop_clicked)
            self.snapshot_button.clicked.connect(self._on_snapshot_clicked)
            
            # Add buttons to layout
            layout.addWidget(self.start_button)
            layout.addWidget(self.stop_button)
            layout.addWidget(self.snapshot_button)
            
            self.setLayout(layout)
            self.logger.debug("Action buttons UI initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize action buttons UI: {str(e)}")
            raise
            
    def _on_start_clicked(self) -> None:
        """Handle start button click event."""
        try:
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.snapshot_button.setEnabled(True)
            self.start_camera.emit()
            self.logger.debug("Start camera signal emitted")
        except Exception as e:
            self.logger.error(f"Error handling start button click: {str(e)}")
            self._reset_button_states()
            
    def _on_stop_clicked(self) -> None:
        """Handle stop button click event."""
        try:
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.snapshot_button.setEnabled(False)
            self.stop_camera.emit()
            self.logger.debug("Stop camera signal emitted")
        except Exception as e:
            self.logger.error(f"Error handling stop button click: {str(e)}")
            self._reset_button_states()
            
    def _on_snapshot_clicked(self) -> None:
        """Handle snapshot button click event."""
        try:
            self.take_snapshot.emit()
            self.logger.debug("Take snapshot signal emitted")
        except Exception as e:
            self.logger.error(f"Error handling snapshot button click: {str(e)}")
            
    def _reset_button_states(self) -> None:
        """Reset all buttons to their default states."""
        try:
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.snapshot_button.setEnabled(False)
            self.logger.debug("Button states reset to default")
        except Exception as e:
            self.logger.error(f"Error resetting button states: {str(e)}")
            
    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable all buttons.

        Args:
            enabled: Whether to enable or disable the buttons
        """
        try:
            self.start_button.setEnabled(enabled)
            self.stop_button.setEnabled(enabled)
            self.snapshot_button.setEnabled(enabled)
            self.logger.debug(
                f"All buttons {'enabled' if enabled else 'disabled'}"
            )
        except Exception as e:
            self.logger.error(
                f"Error setting button enabled states: {str(e)}"
            )
