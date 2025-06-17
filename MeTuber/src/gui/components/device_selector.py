import logging
from typing import List, Optional, Dict, Any
from PyQt5.QtWidgets import (
    QWidget, QComboBox, QFormLayout, QLabel, QHBoxLayout,
    QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal

class DeviceSelector(QWidget):
    """Widget for selecting video input devices."""
    
    device_changed = pyqtSignal(str)
    
    def __init__(self, parent: Optional[QWidget] = None, devices: Optional[List[Dict[str, str]]] = None, default_device: Optional[str] = None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        
        # Initialize UI
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
        # Add label
        self.label = QLabel("Select Camera:")
        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.layout.addWidget(self.label)
        
        # Add combo box
        self.device_combo = QComboBox()
        self.layout.addWidget(self.device_combo)
        
        # Add refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_devices)
        self.layout.addWidget(self.refresh_button)
        
        # Set up device list
        self.devices = devices or []
        self.default_device = default_device
        
        # Initialize devices
        self.set_available_devices(self.devices)
        
        # Connect signals
        self.device_combo.currentTextChanged.connect(self._on_device_changed)
        
    def set_available_devices(self, devices: Optional[List[Dict[str, str]]]) -> None:
        """Set the list of available devices.
        
        Args:
            devices (list): List of device dictionaries with 'name' and 'id' keys
        """
        try:
            self.devices = devices or []
            self.device_combo.clear()
            
            # Add devices to combo box
            for device in self.devices:
                if isinstance(device, dict):
                    name = device.get('name', '')
                    device_id = device.get('id', '')
                    self.device_combo.addItem(name, device_id)
                else:
                    # Handle legacy string format
                    self.device_combo.addItem(str(device), str(device))
                
            # Set default device if provided
            if self.default_device:
                for i in range(self.device_combo.count()):
                    if self.device_combo.itemData(i) == self.default_device:
                        self.device_combo.setCurrentIndex(i)
                        break
                        
            self.logger.info("Device list updated")
            
        except Exception as e:
            self.logger.error(f"Error setting available devices: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to set available devices: {str(e)}"
            )
                    
    def get_selected_device(self) -> str:
        """Get the currently selected device.
        
        Returns:
            str: Selected device ID or empty string if none selected
        """
        return self.device_combo.currentData() or ""
        
    def refresh_devices(self) -> None:
        """Refresh the list of available devices."""
        # This is a placeholder - actual implementation would query the system
        # for available devices. For testing, we'll just use the mock devices.
        self.set_available_devices(self.devices)
        
    def _on_device_changed(self, device_name: str) -> None:
        """Handle device selection change.
        
        Args:
            device_name (str): Selected device name
        """
        device_id = self.device_combo.currentData()
        if device_id:
            self.device_changed.emit(device_id) 