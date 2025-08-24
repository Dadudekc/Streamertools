import logging
import os
from typing import Optional, Dict, Any
import cv2
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QToolBar, QStatusBar, QLabel, QComboBox, QPushButton,
    QMessageBox, QFileDialog, QMenuBar, QMenu, QAction
)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QFont, QIcon
import numpy as np

# Import managers and services
from src.config.settings_manager import SettingsManager
from src.core.device_manager import DeviceManagerFactory
from src.core.style_manager import StyleManager
from src.services.webcam_service import WebcamService

# Import V2 components
from src.gui.components.accessibility_manager import AccessibilityManager
from src.gui.components.v2_style_selector import V2StyleSelector
from src.gui.components.preview_area import PreviewArea
from src.gui.components.help_about import HelpAboutDialog, HelpButton, TooltipManager
from src.gui.components.parameter_controls import ParameterControls
from src.gui.components.action_buttons import ActionButtons

class V2MainWindow(QMainWindow):
    """V2 Main application window with modern layout and accessibility features."""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        # Initialize managers and services
        self.settings_manager = SettingsManager()
        self.device_manager = DeviceManagerFactory.create()
        self.style_manager = StyleManager()
        self.webcam_service = WebcamService()
        
        # Initialize V2 components
        self.accessibility_manager = AccessibilityManager(self)
        self.tooltip_manager = TooltipManager()
        
        # UI components
        self.toolbar = None
        self.status_bar = None
        self.splitter = None
        self.preview_area = None
        self.style_selector = None
        self.parameter_controls = None
        self.action_buttons = None
        self.device_combo = None
        self.help_button = None
        
        # Menu bar
        self.menu_bar = None
        self.file_menu = None
        self.view_menu = None
        self.help_menu = None
        
        # Performance monitoring
        self.performance_timer = QTimer()
        self.performance_timer.timeout.connect(self._update_performance_metrics)
        self.performance_timer.start(1000)  # Update every second
        
        # Initialize UI first
        self.init_ui()
        
        # Connect signals after UI is initialized
        self._connect_signals()
        
        # Load settings
        self.load_settings()
        
        # Apply V2 theme
        self._apply_v2_theme()
        
    def init_ui(self) -> None:
        """Initialize the V2 user interface."""
        try:
            # Set window properties
            self.setWindowTitle("Webcam Filter App V2")
            self.setGeometry(100, 100, 1200, 800)
            self.setMinimumSize(1000, 600)
            
            # Create central widget
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            # Create main layout
            main_layout = QVBoxLayout(central_widget)
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.setSpacing(0)
            
            # Create toolbar
            self._create_toolbar()
            main_layout.addWidget(self.toolbar)
            
            # Connect device selection signal after toolbar is created
            if self.device_combo:
                self.device_combo.currentTextChanged.connect(self._on_device_changed)
            
            # Create splitter for main content
            self.splitter = QSplitter(Qt.Horizontal)
            main_layout.addWidget(self.splitter)
            
            # Create preview area (left side - 60% of width)
            self._create_preview_area()
            
            # Create control panel (right side - 40% of width)
            self._create_control_panel()
            
            # Set splitter proportions (60% preview, 40% controls)
            self.splitter.setSizes([720, 480])
            
            # Create status bar
            self._create_status_bar()
            
            # Create menu bar
            self._create_menu_bar()
            
            # Setup accessibility
            self._setup_accessibility()
            
            self.logger.info("V2 Main Window UI initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing V2 Main Window UI: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to initialize UI: {str(e)}"
            )
    
    def _create_toolbar(self) -> None:
        """Create the main toolbar."""
        try:
            self.toolbar = QToolBar()
            self.toolbar.setMovable(False)
            self.toolbar.setIconSize(QSize(24, 24))
            
            # Device selector
            device_label = QLabel("🎥 Camera:")
            self.toolbar.addWidget(device_label)
            
            self.device_combo = QComboBox()
            self.device_combo.setMinimumWidth(200)
            self.toolbar.addWidget(self.device_combo)
            
            # Refresh devices button
            refresh_button = QPushButton("🔄")
            refresh_button.setToolTip("Refresh device list")
            refresh_button.clicked.connect(self._refresh_devices)
            self.toolbar.addWidget(refresh_button)
            
            self.toolbar.addSeparator()
            
            # Action buttons
            self.action_buttons = ActionButtons()
            self.toolbar.addWidget(self.action_buttons.start_button)
            self.toolbar.addWidget(self.action_buttons.stop_button)
            self.toolbar.addWidget(self.action_buttons.snapshot_button)
            
            self.toolbar.addSeparator()
            
            # Settings button
            settings_button = QPushButton("⚙️")
            settings_button.setToolTip("Settings")
            settings_button.clicked.connect(self._show_settings)
            self.toolbar.addWidget(settings_button)
            
            # Help button
            self.help_button = HelpButton()
            self.toolbar.addWidget(self.help_button)
            
            # Setup tooltips
            self.tooltip_manager.set_widget_tooltip(self.device_combo, "device_selector")
            self.tooltip_manager.set_widget_tooltip(refresh_button, "refresh_devices")
            self.tooltip_manager.set_widget_tooltip(settings_button, "settings_button")
            
        except Exception as e:
            self.logger.error(f"Error creating toolbar: {e}")
    
    def _create_preview_area(self) -> None:
        """Create the preview area."""
        try:
            self.preview_area = PreviewArea()
            self.splitter.addWidget(self.preview_area)
            
            # Connect preview area signals
            self.preview_area.preview_clicked.connect(self._on_preview_clicked)
            self.preview_area.snapshot_requested.connect(self._take_snapshot)
            
            # Setup tooltips
            self.tooltip_manager.set_widget_tooltip(self.preview_area, "preview_area")
            
        except Exception as e:
            self.logger.error(f"Error creating preview area: {e}")
    
    def _create_control_panel(self) -> None:
        """Create the control panel (right side)."""
        try:
            control_widget = QWidget()
            control_layout = QVBoxLayout(control_widget)
            control_layout.setContentsMargins(8, 8, 8, 8)
            control_layout.setSpacing(8)
            
            # Style selector
            self.style_selector = V2StyleSelector()
            control_layout.addWidget(self.style_selector)
            
            # Parameter controls
            self.parameter_controls = ParameterControls(control_widget)
            control_layout.addWidget(self.parameter_controls)
            
            # Add spacer to push controls to top
            control_layout.addStretch()
            
            self.splitter.addWidget(control_widget)
            
            # Setup tooltips
            self.tooltip_manager.set_widget_tooltip(self.style_selector, "style_selector")
            self.tooltip_manager.set_widget_tooltip(self.parameter_controls, "parameter_controls")
            
        except Exception as e:
            self.logger.error(f"Error creating control panel: {e}")
    
    def _create_status_bar(self) -> None:
        """Create the status bar."""
        try:
            self.status_bar = QStatusBar()
            self.setStatusBar(self.status_bar)
            
            # Status label
            self.status_label = QLabel("Ready")
            self.status_bar.addWidget(self.status_label)
            
            # Performance indicators
            self.status_bar.addPermanentWidget(QLabel("|"))
            self.fps_label = QLabel("FPS: 0")
            self.status_bar.addPermanentWidget(self.fps_label)
            
            self.status_bar.addPermanentWidget(QLabel("|"))
            self.cpu_label = QLabel("CPU: 0%")
            self.status_bar.addPermanentWidget(self.cpu_label)
            
            self.status_bar.addPermanentWidget(QLabel("|"))
            self.memory_label = QLabel("Memory: 0 MB")
            self.status_bar.addPermanentWidget(self.memory_label)
            
        except Exception as e:
            self.logger.error(f"Error creating status bar: {e}")
    
    def _create_menu_bar(self) -> None:
        """Create the menu bar."""
        try:
            self.menu_bar = self.menuBar()
            
            # File menu
            self.file_menu = self.menu_bar.addMenu("&File")
            
            save_action = QAction("&Save Settings", self)
            save_action.setShortcut("Ctrl+S")
            save_action.triggered.connect(self.save_settings)
            self.file_menu.addAction(save_action)
            
            load_action = QAction("&Load Settings", self)
            load_action.setShortcut("Ctrl+O")
            load_action.triggered.connect(self.load_settings_dialog)
            self.file_menu.addAction(load_action)
            
            self.file_menu.addSeparator()
            
            exit_action = QAction("E&xit", self)
            exit_action.setShortcut("Ctrl+Q")
            exit_action.triggered.connect(self.close)
            self.file_menu.addAction(exit_action)
            
            # View menu
            self.view_menu = self.menu_bar.addMenu("&View")
            
            # Add accessibility menu
            accessibility_menu = self.accessibility_manager.get_accessibility_menu()
            self.view_menu.addMenu(accessibility_menu)
            
            # Help menu
            self.help_menu = self.menu_bar.addMenu("&Help")
            
            help_action = QAction("&Help & About", self)
            help_action.setShortcut("F1")
            help_action.triggered.connect(self._show_help)
            self.help_menu.addAction(help_action)
            
            about_action = QAction("&About", self)
            about_action.triggered.connect(self._show_about)
            self.help_menu.addAction(about_action)
            
        except Exception as e:
            self.logger.error(f"Error creating menu bar: {e}")
    
    def _setup_accessibility(self) -> None:
        """Setup accessibility features."""
        try:
            # Setup widget accessibility
            self.accessibility_manager.setup_widget_accessibility(
                self.device_combo, "Device Selector", "Select your webcam or camera device"
            )
            self.accessibility_manager.setup_widget_accessibility(
                self.preview_area, "Preview Area", "Live preview of your webcam with applied effects"
            )
            self.accessibility_manager.setup_widget_accessibility(
                self.style_selector, "Style Selector", "Choose effects and styles for your webcam"
            )
            
            # Connect accessibility signals
            self.accessibility_manager.status_changed.connect(self._on_accessibility_status_changed)
            self.accessibility_manager.theme_changed.connect(self._on_theme_changed)
            self.accessibility_manager.font_size_changed.connect(self._on_font_size_changed)
            
        except Exception as e:
            self.logger.error(f"Error setting up accessibility: {e}")
    
    def _connect_signals(self) -> None:
        """Connect all signals and slots."""
        try:
            # Webcam service signals
            self.webcam_service.error_signal.connect(self._on_webcam_error)
            self.webcam_service.info_signal.connect(self._on_webcam_info)
            self.webcam_service.frame_ready.connect(self._on_frame_ready)
            
            # Style selection
            self.style_selector.style_changed.connect(self._on_style_changed)
            self.style_selector.variant_changed.connect(self._on_variant_changed)
            
            # Parameter changes
            self.parameter_controls.parameters_changed.connect(self._on_parameters_changed)
            
            # Action buttons
            self.action_buttons.start_camera.connect(self._start_camera)
            self.action_buttons.stop_camera.connect(self._stop_camera)
            self.action_buttons.take_snapshot.connect(self._take_snapshot)
            
        except Exception as e:
            self.logger.error(f"Error connecting signals: {e}")
    
    def _apply_v2_theme(self) -> None:
        """Apply the V2 theme stylesheet."""
        try:
            # Load and apply the V2 theme
            with open("src/gui/styles/v2_theme.qss", "r") as f:
                self.setStyleSheet(f.read())
            
        except Exception as e:
            self.logger.error(f"Error applying V2 theme: {e}")
    
    def _refresh_devices(self) -> None:
        """Refresh the device list."""
        try:
            devices = self.device_manager.get_devices()
            current_device = self.device_combo.currentText()
            
            self.device_combo.clear()
            
            # Extract device names from the dictionary format
            device_names = []
            for device in devices:
                if isinstance(device, dict) and "name" in device:
                    device_names.append(device["name"])
                elif isinstance(device, str):
                    device_names.append(device)
            
            self.device_combo.addItems(device_names)
            
            # Try to restore previous selection
            if current_device in device_names:
                self.device_combo.setCurrentText(current_device)
            elif device_names:
                self.device_combo.setCurrentText(device_names[0])
            
            self.accessibility_manager.announce_status("Device list refreshed")
            
        except Exception as e:
            self.logger.error(f"Error refreshing devices: {e}")
    
    def _on_preview_clicked(self) -> None:
        """Handle preview area click."""
        try:
            if not self.webcam_service.is_running():
                self._start_camera()
            
        except Exception as e:
            self.logger.error(f"Error handling preview click: {e}")
    
    def _start_camera(self) -> None:
        """Start the webcam service."""
        success = False
        try:
            device_name = self.device_combo.currentText()
            if not device_name:
                QMessageBox.warning(self, "Warning", "Please select a camera device")
            else:
                # Convert device name to device ID
                devices = self.device_manager.get_devices()
                device_id = None
                for device in devices:
                    if isinstance(device, dict) and device.get("name") == device_name:
                        device_id = device.get("id")
                        break
                    elif isinstance(device, str) and device == device_name:
                        device_id = device
                        break

                if not device_id:
                    QMessageBox.critical(self, "Error", f"Device ID not found for {device_name}")
                else:
                    # Get current style and parameters
                    current_style = self.style_selector.get_current_style()
                    current_params = self.parameter_controls.get_parameters()

                    if self.webcam_service.start(device_id, current_style, current_params):
                        self.preview_area.set_playing_state(True)
                        self.action_buttons.start_button.setEnabled(False)
                        self.action_buttons.stop_button.setEnabled(True)
                        self.action_buttons.snapshot_button.setEnabled(True)
                        self.status_label.setText("Camera started")
                        self.accessibility_manager.announce_status("Camera started")
                        success = True
                    else:
                        QMessageBox.critical(self, "Error", "Failed to start camera")

        except Exception as e:
            self.logger.error(f"Error starting camera: {e}")
            QMessageBox.critical(self, "Error", f"Failed to start camera: {str(e)}")
        finally:
            if not success:
                self.action_buttons._reset_button_states()
    
    def _stop_camera(self) -> None:
        """Stop the webcam service."""
        try:
            self.webcam_service.stop()
            self.preview_area.set_playing_state(False)
            self.action_buttons.start_button.setEnabled(True)
            self.action_buttons.stop_button.setEnabled(False)
            self.status_label.setText("Camera stopped")
            self.accessibility_manager.announce_status("Camera stopped")
            
        except Exception as e:
            self.logger.error(f"Error stopping camera: {e}")
    
    def _take_snapshot(self) -> None:
        """Take a snapshot."""
        try:
            if not self.webcam_service.is_running():
                QMessageBox.warning(self, "Warning", "Camera is not running")
                return
            
            # Get current frame
            frame = self.webcam_service.get_last_frame()
            if frame is None:
                QMessageBox.warning(self, "Warning", "No frame available")
                return
            
            # Save snapshot
            filename, _ = QFileDialog.getSaveFileName(
                self, "Save Snapshot", "", "PNG Files (*.png);;JPEG Files (*.jpg)"
            )
            
            if filename:
                cv2.imwrite(filename, frame)
                self.status_label.setText(f"Snapshot saved: {os.path.basename(filename)}")
                self.accessibility_manager.announce_status("Snapshot saved")
            
        except Exception as e:
            self.logger.error(f"Error taking snapshot: {e}")
            QMessageBox.critical(self, "Error", f"Failed to take snapshot: {str(e)}")
    
    def _on_frame_ready(self, frame) -> None:
        """Handle new frame from webcam service."""
        try:
            self.preview_area.update_preview(frame)
            
        except Exception as e:
            self.logger.error(f"Error handling frame: {e}")
    
    def _on_device_changed(self, device: str) -> None:
        """Handle device selection change."""
        try:
            self.settings_manager.set_setting("input_device", device)
            self.accessibility_manager.announce_status(f"Device changed to {device}")
            
        except Exception as e:
            self.logger.error(f"Error handling device change: {e}")
    
    def _on_style_changed(self, category: str, style: str) -> None:
        """Handle style selection change."""
        try:
            self.settings_manager.set_setting("style_category", category)
            self.settings_manager.set_setting("style", style)
            
            # Update parameter controls
            # TODO: Get parameters from style manager
            self.accessibility_manager.announce_status(f"Style changed to {style}")
            
        except Exception as e:
            self.logger.error(f"Error handling style change: {e}")
    
    def _on_variant_changed(self, category: str, style: str, variant: str) -> None:
        """Handle style variant change."""
        try:
            self.settings_manager.set_setting("style_variant", variant)
            self.accessibility_manager.announce_status(f"Variant changed to {variant}")
            
        except Exception as e:
            self.logger.error(f"Error handling variant change: {e}")
    
    def _on_parameters_changed(self, parameters: Dict[str, Any]) -> None:
        """Handle parameter changes."""
        try:
            self.settings_manager.set_setting("parameters", parameters)
            
        except Exception as e:
            self.logger.error(f"Error handling parameter changes: {e}")
    
    def _on_webcam_error(self, message: str) -> None:
        """Handle webcam service errors."""
        try:
            self.preview_area.show_error(message)
            self.status_label.setText(f"Error: {message}")
            self.logger.error(f"Webcam error: {message}")
            
        except Exception as e:
            self.logger.error(f"Error handling webcam error: {e}")
    
    def _on_webcam_info(self, message: str) -> None:
        """Handle webcam service info messages."""
        try:
            self.preview_area.show_info(message)
            self.status_label.setText(message)
            self.logger.info(f"Webcam info: {message}")
            
        except Exception as e:
            self.logger.error(f"Error handling webcam info: {e}")
    
    def _update_performance_metrics(self) -> None:
        """Update performance metrics display."""
        try:
            # TODO: Get actual performance metrics from system
            # For now, use placeholder values
            cpu_usage = 15.0  # Placeholder
            memory_usage = 45.0  # Placeholder
            processing_time = 33.0  # Placeholder
            
            # Update status bar
            self.cpu_label.setText(f"CPU: {cpu_usage:.1f}%")
            self.memory_label.setText(f"Memory: {memory_usage:.0f} MB")
            
            # Update preview area
            self.preview_area.update_performance_metrics(cpu_usage, memory_usage, processing_time)
            
        except Exception as e:
            self.logger.error(f"Error updating performance metrics: {e}")
    
    def _on_accessibility_status_changed(self, message: str) -> None:
        """Handle accessibility status changes."""
        try:
            self.status_label.setText(message)
            
        except Exception as e:
            self.logger.error(f"Error handling accessibility status: {e}")
    
    def _on_theme_changed(self, theme: str) -> None:
        """Handle theme changes."""
        try:
            self.logger.info(f"Theme changed to {theme}")
            
        except Exception as e:
            self.logger.error(f"Error handling theme change: {e}")
    
    def _on_font_size_changed(self, size: int) -> None:
        """Handle font size changes."""
        try:
            self.logger.info(f"Font size changed to {size}")
            
        except Exception as e:
            self.logger.error(f"Error handling font size change: {e}")
    
    def _show_settings(self) -> None:
        """Show settings dialog."""
        try:
            # TODO: Implement settings dialog
            QMessageBox.information(self, "Settings", "Settings dialog not yet implemented")
            
        except Exception as e:
            self.logger.error(f"Error showing settings: {e}")
    
    def _show_help(self) -> None:
        """Show help dialog."""
        try:
            dialog = HelpAboutDialog(self)
            dialog.exec_()
            
        except Exception as e:
            self.logger.error(f"Error showing help: {e}")
    
    def _show_about(self) -> None:
        """Show about dialog."""
        try:
            dialog = HelpAboutDialog(self)
            dialog.tab_widget.setCurrentIndex(2)  # About tab
            dialog.exec_()
            
        except Exception as e:
            self.logger.error(f"Error showing about: {e}")
    
    def load_settings(self) -> None:
        """Load application settings."""
        try:
            # Load device
            device = self.settings_manager.get_setting("input_device")
            if device:
                self.device_combo.setCurrentText(device)
            
            # Load style
            category = self.settings_manager.get_setting("style_category", "Artistic")
            style = self.settings_manager.get_setting("style", "Cartoon")
            variant = self.settings_manager.get_setting("style_variant", "")
            
            self.style_selector.set_current_selection(category, style, variant)
            
            # Load parameters
            parameters = self.settings_manager.get_setting("parameters", {})
            if parameters:
                # TODO: Update parameter controls
                pass
            
            self.logger.info("Settings loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Error loading settings: {e}")
    
    def save_settings(self) -> None:
        """Save application settings."""
        try:
            self.settings_manager.save_settings()
            self.status_label.setText("Settings saved")
            self.accessibility_manager.announce_status("Settings saved")
            
        except Exception as e:
            self.logger.error(f"Error saving settings: {e}")
    
    def load_settings_dialog(self) -> None:
        """Show load settings dialog."""
        try:
            filename, _ = QFileDialog.getOpenFileName(
                self, "Load Settings", "", "JSON Files (*.json)"
            )
            
            if filename:
                # TODO: Implement settings loading from file
                QMessageBox.information(self, "Load Settings", "Settings loading not yet implemented")
            
        except Exception as e:
            self.logger.error(f"Error loading settings dialog: {e}")
    
    def closeEvent(self, event) -> None:
        """Handle window close event."""
        try:
            # Stop webcam service
            if self.webcam_service.is_running():
                self.webcam_service.stop()
            
            # Save settings
            self.save_settings()
            
            # Accept the close event
            event.accept()
            
        except Exception as e:
            self.logger.error(f"Error in close event: {e}")
            event.accept() 