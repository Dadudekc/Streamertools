# File: gui_components/device_selector.py

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QComboBox


class DeviceSelector:
    """
    A GUI component for selecting input devices.
    """
    def __init__(self, parent, devices, default_device):
        self.parent = parent
        self.devices = devices
        self.default_device = default_device
        self.device_combo = QComboBox()

    def create(self):
        layout = QHBoxLayout()
        label = QLabel("Select Input Device:")
        
        # Make the combo box editable
        self.device_combo.setEditable(True)

        # Add devices to the combo box
        self.device_combo.addItems(self.devices)

        # Set the default device if it exists in the list
        if self.default_device in self.devices:
            index = self.devices.index(self.default_device)
            self.device_combo.setCurrentIndex(index)
        else:
            print(f"Warning: Default device '{self.default_device}' not in the device list.")

        layout.addWidget(label)
        layout.addWidget(self.device_combo)
        return layout
