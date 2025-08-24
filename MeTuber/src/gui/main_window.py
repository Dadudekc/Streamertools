import logging
import os
from typing import Optional, Dict, Any
import cv2
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
import numpy as np

from src.config.settings_manager import SettingsManager
from src.core.device_manager import DeviceManagerFactory
from src.core.style_manager import StyleManager
from src.services.webcam_service import WebcamService
from src.gui.components.device_selector import DeviceSelector
from src.gui.components.style_tab_manager import StyleTabManager
from src.gui.components.parameter_controls import ParameterControls
from src.gui.components.action_buttons import ActionButtons

class MainWindow(QMainWindow):
    """Main application window that integrates all components."""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        # Initialize managers and services
        self.settings_manager = SettingsManager()
        self.device_manager = DeviceManagerFactory.create()
        self.style_manager = StyleManager()
        self.webcam_service = WebcamService()
        
        # Initialize UI components
        self.device_selector = None
        self.style_tab_manager = None
        self.parameter_controls = None
        self.action_buttons = None
        self.preview_label = None
        self.status_label = None
        
        # Connect signals
        self.webcam_service.error_signal.connect(self.display_error)
        self.webcam_service.info_signal.connect(self.display_info)
        self.webcam_service.frame_ready.connect(self.update_preview)
        
        # Initialize UI
        self.init_ui()
        
        # Load settings
        self.load_settings()
    
    def init_ui(self) -> None:
        """Initialize the user interface."""
        try:
            self.setWindowTitle("Webcam Style Selector")
            self.setGeometry(100, 100, 800, 600)
            
            # Create central widget and layout
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            layout = QVBoxLayout(central_widget)
            
            # 1. Device Selector
            devices = self.device_manager.get_devices()
            default_device = self.settings_manager.get_setting("input_device")
            self.device_selector = DeviceSelector(self, devices, default_device)
            layout.addWidget(self.device_selector)
            
            # Connect device selection
            self.device_selector.device_changed.connect(self.on_device_changed)
            
            # 2. Style Tab Manager
            categories = self.style_manager.get_categories()
            style_instances = {name: instance for name, instance in self.style_manager.style_instances.items()}
            settings = {"style": self.settings_manager.get_setting("style")}
            self.style_tab_manager = StyleTabManager(self, categories, style_instances, settings)
            layout.addWidget(self.style_tab_manager)
            
            # Connect style change
            self.style_tab_manager.style_changed.connect(self.on_style_changed)
            
            # 3. Parameter Controls
            self.parameter_controls = ParameterControls(self)
            layout.addWidget(self.parameter_controls)
            
            # Connect parameter changes
            self.parameter_controls.parameters_changed.connect(self.on_parameters_changed)
            
            # 4. Action Buttons
            self.action_buttons = ActionButtons(self)
            layout.addWidget(self.action_buttons)

            # Connect action button signals
            self.action_buttons.start_camera.connect(self.start_virtual_camera)
            self.action_buttons.stop_camera.connect(self.stop_virtual_camera)
            self.action_buttons.take_snapshot.connect(self.take_snapshot)
            
            # 5. Status Display
            self.status_label = QLabel("Status: Idle")
            self.status_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.status_label)
            
            # 6. Preview Label
            self.preview_label = QLabel()
            self.preview_label.setAlignment(Qt.AlignCenter)
            self.preview_label.setMinimumSize(640, 480)
            layout.addWidget(self.preview_label)
            
            self.logger.info("UI initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing UI: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to initialize UI: {str(e)}"
            )
    
    def load_settings(self) -> None:
        """Load and apply saved settings."""
        try:
            # Load device
            device = self.settings_manager.get_setting("input_device")
            if device and self.device_manager.validate_device(device):
                self.device_selector.set_available_devices(self.device_manager.get_devices())
                self.device_selector.default_device = device
            
            # Load style
            style_name = self.settings_manager.get_setting("style")
            if style_name:
                self.style_tab_manager.set_current_style(style_name)
                self.on_style_changed(style_name)
            
            self.logger.info("Settings loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Error loading settings: {e}")
            QMessageBox.warning(
                self,
                "Warning",
                f"Failed to load some settings: {str(e)}"
            )
    
    def save_settings(self) -> None:
        """Save current settings."""
        try:
            # Check if components are still valid
            if not self.device_selector or not self.style_tab_manager or not self.parameter_controls:
                self.logger.warning("Cannot save settings: components not initialized")
                return
                
            # Save device
            device = self.device_selector.get_selected_device()
            if device:
                self.settings_manager.set_setting("input_device", device)
            
            # Save style
            style = self.style_tab_manager.get_current_style()
            if style:
                self.settings_manager.set_setting("style", style)
            
            # Save parameters
            if self.parameter_controls.current_style:
                params = self.parameter_controls.get_parameters()
                self.settings_manager.set_style_parameters(
                    self.parameter_controls.current_style.name,
                    params
                )
            
            self.settings_manager.save_settings()
            self.logger.info("Settings saved successfully")
            
        except Exception as e:
            self.logger.error(f"Error saving settings: {e}")
            QMessageBox.warning(
                self,
                "Warning",
                f"Failed to save settings: {str(e)}"
            )
    
    def on_device_changed(self, device_id: str) -> None:
        """Handle device selection change."""
        try:
            if device_id and self.device_manager.validate_device(device_id):
                self.settings_manager.set_setting("input_device", device_id)
                self.display_info(f"Selected device: {device_id}")
            else:
                self.display_error(f"Invalid device: {device_id}")
                
        except Exception as e:
            self.logger.error(f"Error handling device change: {e}")
            self.display_error(f"Error selecting device: {str(e)}")
    
    def on_style_changed(self, style_name: str) -> None:
        """Handle style selection change."""
        try:
            style = self.style_manager.get_style(style_name)
            if not style:
                self.display_error(f"Style not found: {style_name}")
                return
            
            # Update parameter controls
            self.parameter_controls.set_style(style)
            
            # Load saved parameters
            params = self.settings_manager.get_style_parameters(style_name)
            if params:
                self.parameter_controls.set_parameters(params)
                
            self.logger.info(f"Style changed to: {style_name}")
            
        except Exception as e:
            self.logger.error(f"Error handling style change: {e}")
            self.display_error(f"Error changing style: {str(e)}")
    
    def on_parameters_changed(self, params: Dict[str, Any]) -> None:
        """Handle parameter changes."""
        try:
            if self.webcam_service and self.webcam_service.is_running():
                self.webcam_service.update_parameters(params)
                self.logger.debug(f"Updated parameters: {params}")
        except Exception as e:
            self.logger.error(f"Error updating parameters: {e}")
            self.display_error(f"Error updating parameters: {str(e)}")
    
    def start_virtual_camera(self) -> bool:
        """Start the virtual camera with current settings."""
        try:
            device_id = self.device_selector.get_selected_device()
            if not device_id or not self.device_manager.validate_device(device_id):
                self.display_error("No valid device selected")
                if self.action_buttons:
                    self.action_buttons.start_button.setEnabled(True)
                    self.action_buttons.stop_button.setEnabled(False)
                    self.action_buttons.snapshot_button.setEnabled(False)
                return False

            style_name = self.style_tab_manager.get_current_style()
            style = self.style_manager.get_style(style_name) if style_name else None

            params = {}
            if style and self.parameter_controls:
                params = self.parameter_controls.get_parameters()

            if self.webcam_service.start(device_id, style, params):
                self.display_info("Running")
                if self.action_buttons:
                    self.action_buttons.start_button.setEnabled(False)
                    self.action_buttons.stop_button.setEnabled(True)
                    self.action_buttons.snapshot_button.setEnabled(True)
                return True

            self.display_error("Failed to start virtual camera")
            if self.action_buttons:
                self.action_buttons.start_button.setEnabled(True)
                self.action_buttons.stop_button.setEnabled(False)
                self.action_buttons.snapshot_button.setEnabled(False)
            return False

        except Exception as e:
            self.logger.error(f"Error starting virtual camera: {e}")
            self.display_error(f"Error starting virtual camera: {str(e)}")
            if self.action_buttons:
                self.action_buttons.start_button.setEnabled(True)
                self.action_buttons.stop_button.setEnabled(False)
                self.action_buttons.snapshot_button.setEnabled(False)
            return False
    
    def stop_virtual_camera(self) -> None:
        """Stop the virtual camera."""
        try:
            self.webcam_service.stop()
            self.display_info("Idle")
            if self.action_buttons:
                self.action_buttons.start_button.setEnabled(True)
                self.action_buttons.stop_button.setEnabled(False)
                self.action_buttons.snapshot_button.setEnabled(False)

        except Exception as e:
            self.logger.error(f"Error stopping virtual camera: {e}")
            self.display_error(f"Error stopping virtual camera: {str(e)}")
            if self.action_buttons:
                self.action_buttons.start_button.setEnabled(True)
                self.action_buttons.stop_button.setEnabled(False)
                self.action_buttons.snapshot_button.setEnabled(False)
    
    def take_snapshot(self) -> None:
        """Take a snapshot of the current frame."""
        try:
            frame = self.webcam_service.get_last_frame()
            if frame is None:
                self.display_error("No frame available")
                return
            
            # Get save path from user
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Snapshot",
                os.path.expanduser("~/Pictures"),
                "Images (*.png *.jpg *.jpeg)"
            )
            
            if file_path:
                cv2.imwrite(file_path, frame)
                self.display_info(f"Snapshot saved to {file_path}")
                
        except Exception as e:
            self.logger.error(f"Error taking snapshot: {e}")
            self.display_error(f"Error taking snapshot: {str(e)}")
    
    def update_preview(self, frame: np.ndarray) -> None:
        """Update the preview label with a new frame."""
        try:
            # Convert frame to QImage
            height, width = frame.shape[:2]
            bytes_per_line = 3 * width
            q_image = QImage(
                frame.data,
                width,
                height,
                bytes_per_line,
                QImage.Format_RGB888
            ).rgbSwapped()
            
            # Update preview label
            self.preview_label.setPixmap(QPixmap.fromImage(q_image))
            
        except Exception as e:
            self.logger.error(f"Error updating preview: {e}")
    
    def display_error(self, message: str) -> None:
        """Display an error message."""
        self.status_label.setText(f"Error: {message}")
        self.status_label.setStyleSheet("color: red")
        self.logger.error(message)
    
    def display_info(self, message: str) -> None:
        """Display an info message."""
        self.status_label.setText(f"Status: {message}")
        self.status_label.setStyleSheet("color: black")
        self.logger.info(message)
    
    def closeEvent(self, event) -> None:
        """Handle window close event."""
        try:
            # Stop webcam service if running
            if self.webcam_service and self.webcam_service.is_running():
                try:
                    self.webcam_service.stop()
                except Exception as e:
                    self.logger.error(f"Error stopping webcam service: {e}")
            
            # Save settings if components are still valid
            try:
                if self.device_selector and self.style_tab_manager and self.parameter_controls:
                    self.save_settings()
            except Exception as e:
                self.logger.error(f"Error saving settings: {e}")
            
            # Clean up components
            try:
                if self.device_selector:
                    self.device_selector.deleteLater()
                if self.style_tab_manager:
                    self.style_tab_manager.deleteLater()
                if self.parameter_controls:
                    self.parameter_controls.deleteLater()
                if self.action_buttons:
                    self.action_buttons.deleteLater()
                if self.preview_label:
                    self.preview_label.deleteLater()
                if self.status_label:
                    self.status_label.deleteLater()
            except Exception as e:
                self.logger.error(f"Error cleaning up components: {e}")
            
            # Clear references
            self.device_selector = None
            self.style_tab_manager = None
            self.parameter_controls = None
            self.action_buttons = None
            self.preview_label = None
            self.status_label = None
            
            # Accept the close event
            event.accept()
            
        except Exception as e:
            self.logger.error(f"Error during close: {e}")
            event.accept()  # Still accept the close event 