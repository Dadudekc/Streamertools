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
from logging.handlers import RotatingFileHandler
import pkgutil
import importlib
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox,
    QFormLayout, QSlider, QPushButton, QMessageBox, QFileDialog, QComboBox, QTabWidget, QCheckBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import traceback

# Import GUI components
from gui_components.device_selector import DeviceSelector
from gui_components.style_tab_manager import StyleTabManager
from gui_components.parameter_controls import ParameterControls
from gui_components.action_buttons import ActionButtons

# Import the Style base class and one fallback style
from styles.base import Style
from styles.effects.original import Original

# Import the updated classes
# Make sure these files actually exist in your styles/artistic/ folder!
from styles.artistic.advanced_cartoon import AdvancedCartoon      # Updated import
from styles.artistic.advanced_cartoon2 import AdvancedCartoonAnime # Updated import

# Import the updated WebcamThread
from webcam_threading import WebcamThread  # Ensure this path is correct

# =============================================================================
# 1. Config Load/Save
# =============================================================================

CONFIG_FILE = "config.json"

def load_settings():
    """Load settings from a JSON file if it exists; otherwise use defaults."""
    default_settings = {
        "input_device": "video=C270 HD WEBCAM",  # Example default
        "style": "Original",
        "parameters": {},
        "snapshot_dir": os.path.join(os.path.dirname(os.path.abspath(__file__)), 'snapshots') # Add default snapshot directory
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
    Returns a list of fully qualified device names, e.g. ["video=C270 HD WEBCAM", ...].
    """
    devices = []
    cmd = ['ffmpeg', '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy']
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8', errors='ignore')
        for line in output.splitlines():
            line = line.strip()
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
    Dynamically loads all Style subclasses from the styles package and categorizes them.

    Returns:
        tuple: 
            - A dictionary of style instances keyed by their names.
            - A dictionary of categories with lists of style names.
    """
    style_instances = {}
    style_categories = {}

    # List of all style-related packages to scan
    packages_to_scan = ['styles']

    seen_classes = set()

    for pkg_name in packages_to_scan:
        logging.debug(f"Scanning package: {pkg_name}")
        try:
            package = importlib.import_module(pkg_name)
        except ImportError as e:
            logging.error(f"Error loading package {pkg_name}: {e}")
            continue

        for _, modname, ispkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            if ispkg:
                continue

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
                        cls not in seen_classes
                    ):
                        try:
                            instance = cls()  # Instantiate
                            seen_classes.add(cls)

                            category = getattr(instance, "category", "Uncategorized")
                            if category not in style_categories:
                                style_categories[category] = []

                            # Avoid duplicate style names in the same category
                            if instance.name not in style_categories[category]:
                                style_categories[category].append(instance.name)

                            style_instances[instance.name] = instance
                            logging.info(f"Loaded style: {instance.name} (Category: {category})")

                        except Exception as instantiation_error:
                            logging.error(f"Failed to instantiate style '{cls.__name__}': {instantiation_error}")

            except Exception as module_error:
                logging.error(f"Failed to load module '{modname}': {module_error}")

    return style_instances, style_categories

# =============================================================================
# 4. PyQt5 GUI
# =============================================================================

# Debug mode flag (can be set via config or env)
DEBUG_MODE = os.environ.get("METUBER_DEBUG", "0") == "1"

SNAPSHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'snapshots')
if not os.path.exists(SNAPSHOT_DIR):
    os.makedirs(SNAPSHOT_DIR)


def show_error_dialog(parent, message, exc=None):
    """Show a critical error dialog and log the error. If exc is provided, log with traceback."""
    if exc:
        logging.error(message, exc_info=True)
        if DEBUG_MODE:
            message += f"\n\nTraceback:\n{traceback.format_exc()}"
    else:
        logging.error(message)
    QMessageBox.critical(parent, "Error", message)


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
        self.snapshot_dir = self.settings.get('snapshot_dir', SNAPSHOT_DIR)

        # Validate and load settings to ensure no invalid parameters
        self.validate_and_load_settings()

        # Initialize the UI
        self.init_ui()

    def validate_and_load_settings(self):
        """Validate and load settings, resetting invalid parameters as needed."""
        for style_name, style_instance in self.style_instances.items():
            style_params = self.settings.get("parameters", {}).get(style_name, {})
            try:
                validated_params = style_instance.validate_params(style_params)
            except Exception as e:
                logging.warning(f"Invalid parameters for style '{style_name}': {e}. Resetting to defaults.")
                # Reset to defaults using normalized parameters
                validated_params = {
                    param['name']: param.get("default", 0)
                    for param in style_instance.parameters
                }
            # For 'file' type parameters, if the path no longer exists, reset to default
            for param in style_instance.parameters:
                if param.get("type") == "file":
                    file_path = validated_params.get(param["name"], "")
                    if file_path and not os.path.exists(file_path):
                        logging.warning(
                            f"File for parameter '{param['name']}' not found at '{file_path}'. Resetting to default '{param.get('default', '')}'."
                        )
                        validated_params[param['name']] = param.get("default", "")
            self.settings["parameters"][style_name] = validated_params
        save_settings(self.settings)
        # If the UI is initialized, update controls to reflect any changed defaults (e.g. file paths)
        if hasattr(self, 'parameter_controls'):
            self.update_parameter_controls()

    def init_ui(self):
        layout = QVBoxLayout()

        # 1) Device Selector
        devices = list_devices() or ["Enter device manually..."]
        default_device = self.settings.get("input_device", devices[0] if devices else "")
        device_selector = DeviceSelector(self, devices, default_device)
        layout.addLayout(device_selector.create())
        self.device_combo = device_selector.device_combo

        # 2) Style Selector with Categories
        style_tab_manager = StyleTabManager(self, self.style_categories, self.style_instances, self.settings)
        layout.addWidget(style_tab_manager)
        self.style_tab_manager = style_tab_manager

        # Connect style change to parameter update
        style_tab_manager.style_changed.connect(self.update_parameter_controls)

        # 3) Parameter Controls
        self.parameter_controls = ParameterControls(self)
        layout.addWidget(self.parameter_controls)

        # Initialize parameters for whichever style is currently selected
        self.update_parameter_controls()

        # 4) Action Buttons
        action_buttons = ActionButtons(self)
        layout.addLayout(
            action_buttons.create(
                start_callback=self.start_virtual_camera,
                stop_callback=self.stop_virtual_camera,
                snapshot_callback=self.take_snapshot
            )
        )
        self.action_buttons = action_buttons

        # 4.1) Auto Optimize Parameters Button
        self.optimize_button = QPushButton("Auto Optimize Parameters")
        self.optimize_button.clicked.connect(self.auto_optimize_parameters)
        layout.addWidget(self.optimize_button)
        # 4.2) Set Snapshot Directory Button
        self.set_snapshot_dir_button = QPushButton("Set Snapshot Save Folder")
        self.set_snapshot_dir_button.clicked.connect(self.set_snapshot_directory)
        layout.addWidget(self.set_snapshot_dir_button)

        # 4.3) Performance Controls
        performance_group = QGroupBox("Performance Settings")
        performance_layout = QFormLayout()
        
        # Max FPS slider
        self.max_fps_slider = QSlider(Qt.Horizontal)
        self.max_fps_slider.setRange(1, 60)
        self.max_fps_slider.setValue(30)
        self.max_fps_label = QLabel("30")
        self.max_fps_slider.valueChanged.connect(lambda v: self.max_fps_label.setText(str(v)))
        performance_layout.addRow("Max FPS:", self.max_fps_slider)
        performance_layout.addRow("", self.max_fps_label)
        
        # Frame skip slider
        self.frame_skip_slider = QSlider(Qt.Horizontal)
        self.frame_skip_slider.setRange(0, 10)
        self.frame_skip_slider.setValue(0)
        self.frame_skip_label = QLabel("0")
        self.frame_skip_slider.valueChanged.connect(lambda v: self.frame_skip_label.setText(str(v)))
        performance_layout.addRow("Frame Skip:", self.frame_skip_slider)
        performance_layout.addRow("", self.frame_skip_label)
        
        performance_group.setLayout(performance_layout)
        layout.addWidget(performance_group)

        # 5) Status Display
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
            for param in self.current_style.parameters:
                if param["name"] not in self.current_style_params:
                    self.current_style_params[param["name"]] = param.get("default", 0)
            # For 'file' parameters, if the path no longer exists (e.g. file moved), reset to default to update GUI
            for param in self.current_style.parameters:
                if param.get("type") == "file":
                    current_path = self.current_style_params.get(param["name"], "")
                    if current_path and not os.path.exists(current_path):
                        logging.info(
                            f"File for parameter '{param['name']}' not found at '{current_path}', resetting to default '{param.get('default','')}'"
                        )
                        # Reset internal state and update settings
                        new_default = param.get('default', '')
                        self.current_style_params[param['name']] = new_default
                        # Persist change
                        style_name = self.style_tab_manager.get_current_style()
                        self.settings['parameters'][style_name][param['name']] = new_default
                        save_settings(self.settings)

            # Update controls based on normalized parameters list
            self.parameter_controls.update_parameters(
                self.current_style.parameters,
                self.current_style_params,
                self.on_param_changed
            )
        else:
            logging.warning(f"No style found for: {selected_style_name}")

    def on_param_changed(self, param_name, value, widget):
        """
        Handles parameter changes from the UI controls.

        Args:
            param_name (str): The name of the parameter.
            value (int, float, str, bool): The new value of the parameter.
            widget (QWidget): The widget that triggered the change.
        """
        self.current_style_params[param_name] = value
        selected_style_name = self.style_tab_manager.get_current_style()
        if "parameters" not in self.settings:
            self.settings["parameters"] = {}
        self.settings["parameters"][selected_style_name] = self.current_style_params
        save_settings(self.settings)

        # Update label text for sliders/combos/checkboxes
        if isinstance(widget, QLabel):
            try:
                if isinstance(value, int):
                    widget.setText(f"{value}")
                elif isinstance(value, float):
                    widget.setText(f"{value:.1f}")
                else:
                    widget.setText(str(value))
            except Exception as e:
                logging.error(f"Failed to update label for '{param_name}': {e}")
        elif isinstance(widget, QComboBox):
            logging.debug(f"ComboBox '{param_name}' changed to '{value}'")
        elif isinstance(widget, QCheckBox):
            logging.debug(f"Checkbox '{param_name}' changed to '{value}'")
        else:
            logging.debug(f"Parameter '{param_name}' updated to {value} (widget={type(widget)})")

        # If the webcam thread is running, update parameters on the fly
        if self.thread and self.thread.isRunning():
            thread_params = dict(self.current_style_params)
            thread_params['max_fps'] = self.max_fps_slider.value()
            thread_params['frame_skip'] = self.frame_skip_slider.value()
            self.thread.update_params(thread_params)

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

        # Add performance parameters to style params
        thread_params = dict(self.current_style_params)
        thread_params['max_fps'] = self.max_fps_slider.value()
        thread_params['frame_skip'] = self.frame_skip_slider.value()
        
        # Initialize and start the thread
        self.thread = WebcamThread(
            input_device=input_device,
            style_instance=self.style_instances[selected_style],
            style_params=thread_params
        )
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

    def set_snapshot_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Snapshot Save Folder", self.snapshot_dir)
        if dir_path:
            self.snapshot_dir = dir_path
            self.settings['snapshot_dir'] = dir_path
            save_settings(self.settings)

    def take_snapshot(self):
        """Capture the last processed frame and let the user save it."""
        if not self.thread or self.thread.last_frame is None:
            QMessageBox.information(self, "Snapshot", "No frame available to save.")
            return
        default_path = os.path.join(self.snapshot_dir, "snapshot.png")
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Snapshot", default_path, "Image Files (*.png *.jpg *.bmp)")
        if save_path:
            cv2.imwrite(save_path, self.thread.last_frame)
            QMessageBox.information(self, "Snapshot", f"Snapshot saved to:\n{save_path}")
            logging.info(f"Snapshot saved to: {save_path}")

    def display_error(self, message, exc=None):
        """Show error messages via a dialog and stop the thread."""
        show_error_dialog(self, message, exc)
        self.stop_virtual_camera()

    def display_info(self, message):
        """Display status messages in the status label."""
        self.status_label.setText(f"Status: {message}")
        logging.info(f"Info: {message}")

    def auto_optimize_parameters(self):
        """Use AI to find the best parameters for the current style on the last frame."""
        # Ensure there's a frame to optimize on
        if not self.thread or self.thread.last_frame is None:
            show_error_dialog(self, "No frame available for optimization.")
            return
        selected_style = self.current_style
        # Check if the style supports AI optimization
        if not hasattr(selected_style, "ai_optimize"):
            QMessageBox.information(self, "AI Optimize", "Current style does not support AI optimization.")
            return
        try:
            # Run AI optimization on the last captured frame
            optimized_params = selected_style.ai_optimize(self.thread.last_frame, self.current_style_params.copy())
            # Disable recursive AI flag if present
            if "enable_ai_optimization" in optimized_params:
                optimized_params["enable_ai_optimization"] = False
            # Update internal state and UI controls
            self.current_style_params = optimized_params
            self.parameter_controls.update_parameters(
                selected_style.parameters,
                self.current_style_params,
                self.on_param_changed
            )
            # Save optimized parameters
            style_name = self.style_tab_manager.get_current_style()
            self.settings["parameters"][style_name] = self.current_style_params
            save_settings(self.settings)
            QMessageBox.information(self, "AI Optimize", "Parameters optimized and updated.")
        except Exception as e:
            show_error_dialog(self, f"Optimization failed: {e}", exc=e)

    def closeEvent(self, event):
        """Ensure the thread stops when closing the app."""
        if self.thread and self.thread.isRunning():
            self.thread.stop()
            logging.info("Application closed. WebcamThread stopped.")
        event.accept()

# =============================================================================
# 5. Main Function - App Entry Point
# =============================================================================

def main():
    # Setup logging with rotation
    file_handler = RotatingFileHandler(
        "webcam_app.log", maxBytes=5 * 1024 * 1024, backupCount=3
    )
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[file_handler, stream_handler]
    )

    app = QApplication(sys.argv)
    window = WebcamApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
