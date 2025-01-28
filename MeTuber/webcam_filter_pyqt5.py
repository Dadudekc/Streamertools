# webcam_filter_pyqt5.py

import inspect
import sys
import os
import json
import subprocess
import av
import cv2
import numpy as np
import pyvirtualcam
import logging
import pkgutil
import importlib
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox,
    QFormLayout, QSlider, QPushButton, QMessageBox, QFileDialog, QComboBox, QTabWidget
)
from PyQt5.QtCore import Qt

# Import GUI components
from gui_components.device_selector import DeviceSelector
from gui_components.style_tab_manager import StyleTabManager
from gui_components.parameter_controls import ParameterControls
from gui_components.action_buttons import ActionButtons

# Import the Style base class and Original style
from styles.base import Style
from styles.effects.original import Original

# Import the updated WebcamThread
from webcam_threading import WebcamThread

# =============================================================================
# 1. Config Load/Save
# =============================================================================

CONFIG_FILE = "config.json"

def load_settings():
    """Load settings from a JSON file if it exists; otherwise use defaults."""
    default_settings = {
        "input_device": "video=C270 HD WEBCAM",  # Default from your working snippet
        "style": "Original",
        "parameters": {}
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                loaded = json.load(f)
                default_settings.update(loaded)
        except (json.JSONDecodeError, IOError):
            logging.warning("Failed to load config.json. Using default settings.")
    return default_settings

def save_settings(settings):
    """Save current settings to a JSON file."""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(settings, f, indent=4)
    except IOError as e:
        logging.error(f"Error saving settings: {e}")

# =============================================================================
# 2. Device Enumeration (Windows-Only)
# =============================================================================

def list_devices():
    """
    List DirectShow devices on Windows using FFmpeg.
    Returns a list of fully qualified device names, e.g. ["video=C270 HD WEBCAM", "video=OBS Virtual Camera"].
    """
    devices = []
    cmd = ['ffmpeg', '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy']
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8', errors='ignore')
        for line in output.splitlines():
            line = line.strip()  # Remove leading/trailing spaces
            if line.startswith("[dshow") and '"' in line:
                start_idx = line.find('"')
                end_idx = line.rfind('"')
                if start_idx != -1 and end_idx != -1:
                    device_name = line[start_idx + 1:end_idx]
                    devices.append(f"video={device_name}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Could not enumerate devices using FFmpeg: {e}")
    return devices

# =============================================================================
# 3. Dynamic Style Loading
# =============================================================================

def load_styles():
    """
    Dynamically loads all Style subclasses from the styles and adjustments packages and categorizes them.

    Returns:
        tuple: 
            - A dictionary of style instances keyed by their names.
            - A dictionary of categories with lists of unique style names.
    """
    style_instances = {}
    style_categories = {}

    # List of all style-related packages to scan
    packages_to_scan = ['styles']

    seen_classes = set()  # Track loaded classes to prevent duplicates

    for pkg_name in packages_to_scan:
        logging.debug(f"Scanning package: {pkg_name}")
        try:
            package = importlib.import_module(pkg_name)
        except ImportError as e:
            logging.error(f"Error loading package {pkg_name}: {e}")
            continue  # Skip this package and move to the next

        for _, modname, ispkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            if ispkg:
                continue  # Skip sub-packages

            logging.debug(f"Found module: {modname}")
            try:
                module = importlib.import_module(modname)

                for cls_name in dir(module):
                    cls = getattr(module, cls_name)

                    if (
                        inspect.isclass(cls) and
                        issubclass(cls, Style) and
                        cls is not Style and
                        not inspect.isabstract(cls) and
                        cls not in seen_classes  # Prevent duplicate entries
                    ):
                        try:
                            instance = cls()  # Attempt to instantiate
                            seen_classes.add(cls)

                            category = getattr(instance, "category", "Uncategorized")
                            if category not in style_categories:
                                style_categories[category] = []

                            if instance.name not in style_categories[category]:  # Avoid duplicate names
                                style_categories[category].append(instance.name)

                            style_instances[instance.name] = instance
                            logging.info(f"Loaded style: {instance.name} under category: {category}")

                        except Exception as instantiation_error:
                            logging.error(f"Failed to instantiate style '{cls.__name__}': {instantiation_error}")

            except Exception as module_error:
                logging.error(f"Failed to load module '{modname}': {module_error}")

    return style_instances, style_categories


# =============================================================================
# 4. PyQt5 GUI
# =============================================================================

class WebcamApp(QWidget):
    """
    Main GUI application that manages device selection, style parameters,
    and the start/stop logic for the webcam processing thread.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Webcam Style Selector")
        self.setGeometry(100, 100, 800, 600)

        # Thread & style management
        self.thread = None
        self.style_instances, self.style_categories = load_styles()
        self.current_style = None
        self.current_style_params = {}

        # Config settings
        self.settings = load_settings()

        # Validate and load settings to ensure no invalid parameters
        self.validate_and_load_settings()

        # Initialize the UI
        self.init_ui()

    def validate_and_load_settings(self):
        """Validate and load settings, resetting invalid parameters."""
        for style_name, style_instance in self.style_instances.items():
            style_params = self.settings.get("parameters", {}).get(style_name, {})
            try:
                validated_params = style_instance.validate_params(style_params)
            except Exception as e:
                logging.warning(f"Invalid parameters for style '{style_name}': {e}. Resetting to defaults.")
                validated_params = {param['name']: param['default'] for param in style_instance.define_parameters()}
            self.settings["parameters"][style_name] = validated_params
        save_settings(self.settings)

    def init_ui(self):
        layout = QVBoxLayout()

        # 5.1 Device Selector
        devices = list_devices() or ["Enter device manually..."]
        default_device = self.settings.get("input_device", devices[0] if devices else "")
        device_selector = DeviceSelector(self, devices, default_device)
        layout.addLayout(device_selector.create())
        self.device_combo = device_selector.device_combo

        # 5.2 Style Selector with Categories
        style_tab_manager = StyleTabManager(self, self.style_categories, self.style_instances, self.settings)
        layout.addWidget(style_tab_manager)
        self.style_tab_manager = style_tab_manager

        # Connect style change to parameter update via the new signal
        style_tab_manager.style_changed.connect(self.update_parameter_controls)

        # 5.3 Parameter Controls
        self.parameter_controls = ParameterControls(self)
        layout.addWidget(self.parameter_controls)
        # Initialize parameters based on the selected style
        self.update_parameter_controls()

        # 5.4 Action Buttons
        action_buttons = ActionButtons(self)
        layout.addLayout(action_buttons.create(self.start_virtual_camera, self.stop_virtual_camera, self.take_snapshot))
        self.action_buttons = action_buttons  # Store reference for enabling/disabling

        # 5.5 Status Display
        self.status_label = QLabel("Status: Idle")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def update_parameter_controls(self):
        """Update parameter controls based on the selected style."""
        selected_style_name = self.style_tab_manager.get_current_style()
        self.current_style = self.style_instances.get(selected_style_name, Original())

        saved_params = self.settings.get("parameters", {})
        self.current_style_params = saved_params.get(selected_style_name, {}).copy()

        if self.current_style:
            logging.info(f"Updating parameters for style: {selected_style_name}")
            
            # Ensure all parameters have default values if missing
            for param in self.current_style.define_parameters():
                if param["name"] not in self.current_style_params:
                    self.current_style_params[param["name"]] = param.get("default", 0)
            
            self.parameter_controls.update_parameters(
                self.current_style.define_parameters(),
                self.current_style_params,
                self.on_param_changed
            )
        else:
            logging.warning(f"No style found for: {selected_style_name}")

    def on_param_changed(self, param_name, value, label_widget):
        """
        Update the parameter in real-time and pass it to the running thread
        so the style changes reflect immediately.
        """
        self.current_style_params[param_name] = value
        label_widget.setText(f"{value}" if isinstance(value, int) else f"{value:.1f}")

        # Save the updated parameter
        selected_style_name = self.style_tab_manager.get_current_style()
        if "parameters" not in self.settings:
            self.settings["parameters"] = {}
        self.settings["parameters"][selected_style_name] = self.current_style_params
        save_settings(self.settings)

        # If the thread is running, update parameters on the fly
        if self.thread and self.thread.isRunning():
            self.thread.update_params(dict(self.current_style_params))

    def start_virtual_camera(self):
        """Starts the WebcamThread to capture frames via PyAV and stream them."""
        input_device = self.device_combo.currentText().strip()
        selected_style = self.style_tab_manager.get_current_style()

        if not input_device:
            QMessageBox.warning(self, "Input Device Error", "Please specify a valid input device.")
            return

        if not selected_style:
            QMessageBox.warning(self, "Style Selection Error", "Please select a style.")
            return

        # Save current settings
        self.settings["input_device"] = input_device
        self.settings["style"] = selected_style
        if "parameters" not in self.settings:
            self.settings["parameters"] = {}
        self.settings["parameters"][selected_style] = self.current_style_params
        save_settings(self.settings)

        # Initialize and start the thread
        self.thread = WebcamThread(input_device, self.current_style, dict(self.current_style_params))
        self.thread.error_signal.connect(self.display_error)
        self.thread.info_signal.connect(self.display_info)
        self.thread.start()

        # Update button states
        self.action_buttons.start_button.setEnabled(False)
        self.action_buttons.stop_button.setEnabled(True)
        self.action_buttons.snapshot_button.setEnabled(True)
        self.status_label.setText("Status: Running")
        logging.info("Virtual camera started.")

    def stop_virtual_camera(self):
        """Stops the webcam thread."""
        if self.thread:
            self.thread.stop()
            self.thread = None
            self.status_label.setText("Status: Stopped")
            logging.info("Virtual camera stopped.")

        # Update button states
        self.action_buttons.start_button.setEnabled(True)
        self.action_buttons.stop_button.setEnabled(False)
        self.action_buttons.snapshot_button.setEnabled(False)

    def take_snapshot(self):
        """
        Capture the last processed frame and let the user save it.
        """
        if not self.thread or self.thread.last_frame is None:
            QMessageBox.information(self, "Snapshot", "No frame available to save.")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save Snapshot", "", "Image Files (*.png *.jpg *.bmp)")
        if save_path:
            cv2.imwrite(save_path, self.thread.last_frame)
            QMessageBox.information(self, "Snapshot", f"Snapshot saved to:\n{save_path}")
            logging.info(f"Snapshot saved to: {save_path}")

    def display_error(self, message):
        """Show error messages via a dialog and stop the thread."""
        QMessageBox.critical(self, "Error", message)
        self.stop_virtual_camera()

    def display_info(self, message):
        """Display status messages in the status label."""
        self.status_label.setText(f"Status: {message}")
        logging.info(f"Info: {message}")

    def closeEvent(self, event):
        """Ensure the thread stops when closing the app."""
        if self.thread and self.thread.isRunning():
            self.thread.stop()
            logging.info("Application closed. WebcamThread stopped.")
        event.accept()

def main():
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG,  # Set to DEBUG for detailed logging
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("webcam_app.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

    app = QApplication(sys.argv)
    window = WebcamApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

